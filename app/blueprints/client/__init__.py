from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from datetime import date, datetime
from sqlalchemy import select
from db import ContoCorrente, RichiestaContoCorrente, db
from db import Prestito, Cliente, Garanzia
from utils.decorators import client_auth_required, client_unauth_required
from utils.storage import save_file
from .forms import LoginForm, AccountForm, PrestitoForm


client_page = Blueprint('client', __name__, template_folder="templates/client")


@client_page.route('/login', methods=['GET', 'POST'])
@client_unauth_required
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data

            client = Cliente.query.filter_by(email=email).first()

            if client:
                # check if the password is correct
                if client.verify_password(password):
                    flash('Login successful!', 'success')
                    session['client'] = client.serialize()
                    return redirect(url_for('client.dashboard'))

                flash('Invalid email or password', 'danger')
            else:
                flash('Invalid email or password', 'danger')

    return render_template('login.html', login_form=login_form)


@client_page.route('/logout', methods=['GET'])
@client_auth_required
def logout():
    session.pop('client', None)
    return redirect(url_for('client.login'))


@client_page.route('/dashboard', methods=['GET'])
@client_auth_required
def dashboard():
    richieste_in_attesa = RichiestaContoCorrente.query.filter(
        RichiestaContoCorrente.cliente_id == session['client']['id'],
        RichiestaContoCorrente.accettata == None
    ).count()
    conti_correnti = ContoCorrente.query.filter(
        (ContoCorrente.client1_id == session['client']['id']) | (
            ContoCorrente.client2_id == session['client']['id'])
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
        richiesta.cliente_id = session['client']['id']
        db.session.add(richiesta)

        try:
            db.session.commit()
            flash('Richiesta inviata con successo.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error durante l\'invio della richiesta: {e}', 'error')

    return redirect(url_for('client.dashboard'))

@client_page.route('/conto_corrente', methods=['POST'])
@client_auth_required
def conto_corrente():
    if request.method == 'POST':
        email = request.form.get('email')
        stmt = select(Cliente).where(Cliente.email == email)
        client = db.session.scalar(stmt)
        if not client:
            flash('Utente non trovato.', 'danger')
            return redirect(url_for('client.dashboard'))

        # add user as second client
        stmt = select(ContoCorrente).where(
            ContoCorrente.client1_id == session['client']['id']
        ).where(
            ContoCorrente.id == request.form.get('id')
        )
        conto_corrente = db.session.scalar(stmt)

        if not conto_corrente:
            flash('Conto corrente non trovato.', 'danger')
            return redirect(url_for('client.dashboard'))

        conto_corrente.client2_id = client.id
        db.session.add(conto_corrente)
        
        try:
            db.session.commit()
            flash('Utente aggiunto al conto corrente con successo.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error durante l\'aggiornamento: {e}', 'error')

    return redirect(url_for('client.dashboard'))


@client_page.route('/prestiti', methods=['GET', 'POST'])
@client_auth_required
def prestiti():
    form = PrestitoForm()

    if form.validate_on_submit():
        # create the prestito
        prestito = Prestito()
        prestito.importo = form.importo.data
        prestito.cliente_id = session['client']['id']

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
        cliente_id=session['client']['id']).all()

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
        session["client"]["data_nascita"], '%a, %d %b %Y %H:%M:%S %Z')
    data_nascita = date(data_nascita.year,
                        data_nascita.month, data_nascita.day)
    session["client"]["data_nascita"] = data_nascita

    if request.method == 'POST':
        if form.validate_on_submit():
            id = session["client"]["id"]

            # find client
            stmt = select(Cliente).where(Cliente.id == id)
            client = db.session.scalar(stmt)

            if not client:
                return redirect(url_for('client.logout'))

            # update the client's information with form data
            client.codice_fiscale = form.codice_fiscale.data
            client.nome = form.nome.data
            client.cognome = form.cognome.data
            client.data_nascita = form.data_nascita.data
            client.indirizzo = form.indirizzo.data
            client.telefono = form.telefono.data

            if form.password.data:
                client.set_password(form.password.data)

            # commit the changes to the database
            try:
                db.session.commit()
                session["client"] = client.serialize()
                flash('Account aggiornato con successo.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error durante l\'aggiornamento: {e}', 'error')

    return render_template('account.html', account_form=form)
