from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from datetime import date, datetime
from sqlalchemy import select
from db import ContoCorrente, RichiestaContoCorrente, db
from db import Prestito, Cliente, Garanzia
from utils.decorators import client_auth_required, client_unauth_required
from utils.storage import save_file
from .forms import LoginForm, AccountForm, PrestitoForm


client_page = Blueprint('cliente', __name__, template_folder="templates/cliente")


@client_page.route('/login', methods=['GET', 'POST'])
@client_unauth_required
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data

            cliente = Cliente.query.filter_by(email=email).first()

            if cliente:
                # check if the password is correct
                if cliente.verify_password(password):
                    flash('Login successful!', 'success')
                    session['cliente'] = cliente.serialize()
                    return redirect(url_for('cliente.dashboard'))

                flash('Invalid email or password', 'danger')
            else:
                flash('Invalid email or password', 'danger')

    return render_template('login.html', login_form=login_form)


@client_page.route('/logout', methods=['GET'])
@client_auth_required
def logout():
    session.pop('cliente', None)
    return redirect(url_for('cliente.login'))


@client_page.route('/dashboard', methods=['GET'])
@client_auth_required
def dashboard():
    richieste_in_attesa = RichiestaContoCorrente.query.filter(
        RichiestaContoCorrente.cliente_id == session['cliente']['id'],
        RichiestaContoCorrente.accettata == None
    ).count()
    conti_correnti = ContoCorrente.query.filter(
        (ContoCorrente.client1_id == session['cliente']['id']) | (
            ContoCorrente.client2_id == session['cliente']['id'])
    ).all()

    return render_template(
        'dashboard.html',
        richieste_in_attesa=richieste_in_attesa,
        conti_correnti=conti_correnti
    )

@client_page.route('/richiesta_conto_corrente', methods=['POST'])
@client_auth_required
def richiesta_conto_corrente():
    if request.method == 'POST':
        richiesta = RichiestaContoCorrente()
        richiesta.cliente_id = session['cliente']['id']
        db.session.add(richiesta)

        try:
            db.session.commit()
            flash('Richiesta inviata con successo.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error durante l\'invio della richiesta: {e}', 'error')

    return redirect(url_for('cliente.dashboard'))

@client_page.route('/conto_corrente', methods=['POST'])
@client_auth_required
def conto_corrente():
    if request.method == 'POST':
        email = request.form.get('email')
        stmt = select(Cliente).where(Cliente.email == email)
        cliente = db.session.scalar(stmt)
        if not cliente:
            flash('Utente non trovato.', 'danger')
            return redirect(url_for('cliente.dashboard'))

        # add user as second cliente
        stmt = select(ContoCorrente).where(
            ContoCorrente.client1_id == session['cliente']['id']
        ).where(
            ContoCorrente.id == request.form.get('id')
        )
        conto_corrente = db.session.scalar(stmt)

        if not conto_corrente:
            flash('Conto corrente non trovato.', 'danger')
            return redirect(url_for('cliente.dashboard'))

        conto_corrente.client2_id = cliente.id
        db.session.add(conto_corrente)
        
        try:
            db.session.commit()
            flash('Utente aggiunto al conto corrente con successo.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error durante l\'aggiornamento: {e}', 'error')

    return redirect(url_for('cliente.dashboard'))


@client_page.route('/prestiti', methods=['GET', 'POST'])
@client_auth_required
def prestiti():
    form = PrestitoForm()

    if form.validate_on_submit():
        # create the prestito
        prestito = Prestito()
        prestito.importo = form.importo.data
        prestito.cliente_id = session['cliente']['id']

        db.session.add(prestito)
        db.session.commit()

        # create each garanzia
        for garanzia in form.garanzie:
            g = Garanzia()
            g.tipologia = garanzia.tipologia.data
            g.valutazione = garanzia.valutazione.data
            g.prestito_id = prestito.id

            # save the file
            file = garanzia.file.data
            path = save_file(file)

            # set the file path
            g.file = path  # type: ignore

            db.session.add(g)

        try:
            db.session.commit()
            flash('Richiesta di prestito salvata con successo.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error durante il salvataggio: {e}')

    prestiti = Prestito.query.filter_by(
        cliente_id=session['cliente']['id']).all()

    return render_template('prestiti.html', prestito_form=form, prestiti=prestiti)


@client_page.route('/carte', methods=['GET'])
@client_auth_required
def carte():
    return render_template('carte.html')


@client_page.route('/azioni', methods=['GET'])
@client_auth_required
def azioni():
    return render_template('azioni.html')


@client_page.route('/account', methods=['GET', 'POST'])
@client_auth_required
def account():
    form = AccountForm()

    # transform date format
    data_nascita = datetime.strptime(
        session["cliente"]["data_nascita"], '%a, %d %b %Y %H:%M:%S %Z')
    data_nascita = date(data_nascita.year,
                        data_nascita.month, data_nascita.day)
    session["cliente"]["data_nascita"] = data_nascita

    if request.method == 'POST':
        if form.validate_on_submit():
            id = session["cliente"]["id"]

            # find cliente
            stmt = select(Cliente).where(Cliente.id == id)
            cliente = db.session.scalar(stmt)

            if not cliente:
                return redirect(url_for('cliente.logout'))

            # update the cliente's information with form data
            cliente.codice_fiscale = form.codice_fiscale.data
            cliente.nome = form.nome.data
            cliente.cognome = form.cognome.data
            cliente.data_nascita = form.data_nascita.data
            cliente.indirizzo = form.indirizzo.data
            cliente.telefono = form.telefono.data

            if form.password.data:
                cliente.set_password(form.password.data)

            # commit the changes to the database
            try:
                db.session.commit()
                session["cliente"] = cliente.serialize()
                flash('Account aggiornato con successo.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error durante l\'aggiornamento: {e}', 'error')

    return render_template('account.html', account_form=form)
