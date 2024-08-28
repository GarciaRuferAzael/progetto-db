from datetime import date, datetime
from flask import Blueprint, Response, flash, redirect, render_template, request, session, url_for
from sqlalchemy import select

from db import Bancario, ContoCorrente, Filiale, Garanzia, Prestito, Transazione, TransazioneInterna, db, Direttore
from db.query import get_conti_correnti_by_direttore_id, get_filiale_by_direttore_id, get_most_spending_clients_for_filiale
from utils.decorators import direttore_auth_required, direttore_unauth_required
from utils.storage import get_mime_type
from .forms import AccountForm, LoginForm


direttore_page = Blueprint('direttore', __name__, template_folder="templates")


@direttore_page.route('/login', methods=['GET', 'POST'])
@direttore_unauth_required
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data

            direttore = Direttore.query.filter_by(email=email).first()

            if direttore:
                # check if the password is correct
                if direttore.verify_password(password):
                    flash('Login successful!', 'success')
                    session['direttore'] = direttore.serialize()
                    return redirect(url_for('direttore.dashboard'))

                flash('Invalid email or password', 'danger')
            else:
                flash('Invalid email or password', 'danger')

    return render_template('direttore/login.html', login_form=login_form)


@direttore_page.route('/logout', methods=['GET'])
@direttore_auth_required
def logout():
    session.pop('direttore', None)
    return redirect(url_for('direttore.login'))


@direttore_page.route('/dashboard', methods=['GET'])
@direttore_auth_required
def dashboard():
    direttore = db.session.query(Direttore).where(
        Direttore.id == session["direttore"]["id"]).first()
    if not direttore:
        return redirect(url_for('direttore.logout'))

    conti_correnti = get_conti_correnti_by_direttore_id(
        session["direttore"]["id"])
    filiale = direttore.filiale

    bancari = filiale.bancari  # type: ignore
    # order bancari by richieste_conti_correnti
    bancari = sorted(bancari, key=lambda b: len(
        list(b.richieste_conti_correnti)), reverse=True)

    most_spending_clients = [{"id": cliente.id, "spesa_totale": cliente.spesa_totale, "nome": cliente.nome + #type: ignore
                              " " + cliente.cognome} for cliente in get_most_spending_clients_for_filiale(filiale.id)] #type: ignore

    return render_template(
        'direttore/dashboard.html',
        conti_correnti=conti_correnti,
        filiale=filiale,
        bancari=bancari,
        most_spending_clients=most_spending_clients
    )


@direttore_page.route('/richieste', methods=['GET'])
@direttore_auth_required
def richieste():
    direttore = db.session.query(Direttore).where(
        Direttore.id == session["direttore"]["id"]).first()

    if not direttore:
        return redirect(url_for('direttore.logout'))

    filiale = direttore.filiale
    prestiti = filiale.prestiti  # type: ignore

    return render_template('direttore/richieste.html', filiale=filiale, prestiti=prestiti)


@direttore_page.route('/accetta_prestito', methods=['POST'])
@direttore_auth_required
def accetta_prestito():
    prestito_id = request.form.get('prestito_id', type=int)
    accettata = bool(request.form.get('accettata', type=int))
    prestito = db.session.query(Prestito).where(
        Prestito.id == prestito_id).first()

    # get filiale
    filiale = get_filiale_by_direttore_id(session['direttore']['id'])
    if not filiale:
        flash('Filiale non trovata', 'danger')
        return redirect(url_for('direttore.richieste'))

    if prestito:
        importo_prestito = int(prestito.importo)  # type: ignore

        if importo_prestito > filiale.saldo:  # type: ignore
            flash("Saldo filiale insufficiente")
            return redirect(url_for('direttore.richieste'))

        prestito.accettata = accettata  # type: ignore
        prestito.data_accettazione = db.func.now()
        prestito.direttore_id = session['direttore']['id']
        db.session.add(prestito)

        conto_corrente = db.session.query(ContoCorrente).where(
            ContoCorrente.id == prestito.conto_corrente_id).first()
        if not conto_corrente:
            flash("Conto corrente di destinazione non valido")
            return redirect(url_for('direttore.richieste'))

        if accettata:
            # withdraw money from the filiale and add them to the conto_corrente
            filiale.saldo -= importo_prestito  # type: ignore
            conto_corrente.saldo += importo_prestito  # type: ignore

            # create transazione
            ti = TransazioneInterna()
            ti.conto_corrente_id = conto_corrente.id

            db.session.add(ti)
            db.session.flush()

            transazione = Transazione()
            transazione.importo = importo_prestito  # type: ignore
            transazione.descrizione = 'Prestito n. ' + \
                str(prestito.id)  # type: ignore
            transazione.transazione_interna_id = ti.id
            transazione.entrata = True  # type: ignore

            db.session.add(transazione)
            db.session.add(filiale)
            db.session.add(conto_corrente)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Errore durante l\'elaborazione della prestito', 'danger')
            print(e)
            return redirect(url_for('direttore.richieste'))

        flash('prestito accettata' if accettata else 'prestito rifutata', 'success')
    else:
        flash('prestito non trovata', 'danger')

    return redirect(url_for('direttore.richieste'))


@direttore_page.route('/garanzia', methods=["GET"])
@direttore_auth_required
def garanzia():
    garanzia_id = request.args.get('garanzia_id', type=int)
    garanzia = db.session.query(Garanzia).where(
        Garanzia.id == garanzia_id).first()

    if not garanzia:
        flash('Garanzia non trovata', 'danger')
        return redirect(url_for('direttore.dashboard'))

    # read the file
    with open(str(garanzia.file), 'rb') as file:
        file_content = file.read()

    # get content type of the file by its content
    mime = get_mime_type(str(garanzia.file))

    return Response(file_content, mimetype=mime)


@direttore_page.route('/account', methods=['GET', 'POST'])
@direttore_auth_required
def account():
    form = AccountForm()

    # transform date format
    data_nascita = datetime.strptime(
        session["direttore"]["data_nascita"], '%a, %d %b %Y %H:%M:%S %Z')
    data_nascita = date(data_nascita.year,
                        data_nascita.month, data_nascita.day)
    session["direttore"]["data_nascita"] = data_nascita

    if request.method == 'POST':
        if form.validate_on_submit():
            id = session["direttore"]["id"]

            # find direttore
            stmt = select(Direttore).where(Direttore.id == id)
            direttore = db.session.scalar(stmt)

            if not direttore:
                return redirect(url_for('direttore.logout'))

            # update the direttore's information with form data
            direttore.codice_fiscale = form.codice_fiscale.data
            direttore.nome = form.nome.data
            direttore.cognome = form.cognome.data
            direttore.data_nascita = form.data_nascita.data
            direttore.indirizzo = form.indirizzo.data
            direttore.telefono = form.telefono.data

            if form.password.data:
                direttore.set_password(form.password.data)

            # commit the changes to the database
            try:
                db.session.commit()
                session["direttore"] = direttore.serialize()
                flash('Account aggiornato con successo.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error durante l\'aggiornamento: {e}', 'error')

    return render_template('direttore/account.html', account_form=form)
