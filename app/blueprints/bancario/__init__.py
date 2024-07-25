from xmlrpc.client import boolean
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from db import ContoCorrente, db, Bancario, RichiestaContoCorrente
from utils.decorators import bancario_auth_required, bancario_unauth_required
from .forms import LoginForm


bancario_page = Blueprint('bancario', __name__, template_folder="templates")

@bancario_page.route('/login', methods=['GET', 'POST'])
@bancario_unauth_required
def login():
    login_form = LoginForm()
    
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data

            bancario = Bancario.query.filter_by(email=email).first()

            if bancario:
                # check if the password is correct
                if bancario.verify_password(password):
                    flash('Login successful!', 'success')
                    session['bancario'] = bancario.serialize()
                    return redirect(url_for('bancario.dashboard'))

                flash('Invalid email or password', 'danger')
            else:
                flash('Invalid email or password', 'danger')

    return render_template('bancario/login.html', login_form=login_form)

@bancario_page.route('/logout', methods=['GET'])
@bancario_auth_required
def logout():
    session.pop('bancario', None)
    return redirect(url_for('bancario.login'))

@bancario_page.route('/dashboard', methods=['GET'])
@bancario_auth_required
def dashboard():
    return render_template('bancario/dashboard.html')

@bancario_page.route('/richieste', methods=['GET'])
@bancario_auth_required
def richieste():
    richieste = RichiestaContoCorrente.query.filter(RichiestaContoCorrente.accettata == None).all()
    return render_template('bancario/richieste.html', richieste=richieste)

@bancario_page.route('/accetta_richiesta', methods=['POST'])
@bancario_auth_required
def accetta_richiesta():
    richiesta_id = request.form.get('richiesta_id', type=int)
    accettata = bool(request.form.get('accettata', type=int))
    richiesta = RichiestaContoCorrente.query.filter_by(id=richiesta_id).first()

    print("Accettata", accettata)


    if richiesta:
        richiesta.accettata = accettata
        richiesta.data_accettazione = db.func.now()
        richiesta.bancario_id = session['bancario']['id']
        db.session.add(richiesta)
        
        if accettata:
            # create a new conto corrente
            conto = ContoCorrente()
            conto.client1_id = richiesta.cliente_id
            conto.filiale_id = session['bancario']['filiale_id']
            
            db.session.add(conto)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Errore durante l\'elaborazione della richiesta', 'danger')
            print(e)
            return redirect(url_for('bancario.richieste'))
        
        flash('Richiesta accettata' if accettata else 'Richiesta rifutata', 'success')
    else:
        flash('Richiesta non trovata', 'danger')

    return redirect(url_for('bancario.richieste'))