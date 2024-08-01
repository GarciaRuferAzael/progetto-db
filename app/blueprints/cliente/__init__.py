from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from datetime import date, datetime
from sqlalchemy import select
from db import ContoCorrente, RichiestaContoCorrente, Transazione, TransazioneEsterna, TransazioneInterna, db
from db import Prestito, Cliente, Garanzia
from db.query import get_transazioni_by_conto_corrente_id
from utils.decorators import cliente_auth_required, cliente_unauth_required
from utils.storage import save_file
from .forms import BonificoForm, LoginForm, AccountForm, PrestitoForm


client_page = Blueprint('cliente', __name__, template_folder="templates")


@client_page.route('/login', methods=['GET', 'POST'])
@cliente_unauth_required
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

    return render_template('cliente/login.html', login_form=login_form)


@client_page.route('/logout', methods=['GET'])
@cliente_auth_required
def logout():
    session.pop('cliente', None)
    return redirect(url_for('cliente.login'))


@client_page.route('/dashboard', methods=['GET'])
@cliente_auth_required
def dashboard():
    richieste_in_attesa = RichiestaContoCorrente.query.filter(
        RichiestaContoCorrente.cliente_id == session['cliente']['id'],
        RichiestaContoCorrente.accettata == None
    ).count()
    conti_correnti = ContoCorrente.query.filter(
        (ContoCorrente.cliente1_id == session['cliente']['id']) | (
            ContoCorrente.cliente2_id == session['cliente']['id'])
    ).all()

    return render_template(
        'cliente/dashboard.html',
        richieste_in_attesa=richieste_in_attesa,
        conti_correnti=conti_correnti
    )


@client_page.route('/richiesta_conto_corrente', methods=['POST'])
@cliente_auth_required
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


@client_page.route('/add_user_conto_corrente', methods=['POST'])
@cliente_auth_required
def add_user_conto_corrente():
    if request.method == 'POST':
        email = request.form.get('email')
        stmt = select(Cliente).where(Cliente.email == email)
        cliente = db.session.scalar(stmt)
        if not cliente:
            flash('Utente non trovato.', 'danger')
            return redirect(url_for('cliente.dashboard'))

        # add user as second cliente
        stmt = select(ContoCorrente).where(
            ContoCorrente.cliente1_id == session['cliente']['id']
        ).where(
            ContoCorrente.id == request.form.get('id')
        )
        conto_corrente = db.session.scalar(stmt)

        if not conto_corrente:
            flash('Conto corrente non trovato.', 'danger')
            return redirect(url_for('cliente.dashboard'))

        conto_corrente.cliente2_id = cliente.id
        db.session.add(conto_corrente)

        try:
            db.session.commit()
            flash('Utente aggiunto al conto corrente con successo.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error durante l\'aggiornamento: {e}', 'error')

    return redirect(url_for('cliente.dashboard'))


@client_page.route('/conto_corrente/<int:id>', methods=['GET'])
@cliente_auth_required
def conto_corrente(id):
    form = BonificoForm()
    
    stmt = select(ContoCorrente).where(ContoCorrente.id == id)
    conto_corrente = db.session.scalar(stmt)

    if not conto_corrente:
        flash('Conto corrente non trovato.', 'danger')
        return redirect(url_for('cliente.dashboard'))

    # get transactions for the conto corrente
    transazioni = get_transazioni_by_conto_corrente_id(conto_corrente.id)
    t_list = [
        {"data": t.data.strftime('%Y-%m-%d %H:%M:%S'), "importo": t.importo, "entrata": t.entrata}
        for t in transazioni
    ]

    return render_template(
        'cliente/conto_corrente.html',
        conto_corrente=conto_corrente, 
        transazioni=transazioni,
        t_list=t_list,
        bonifico_form=form
    )

@client_page.route('/bonifico', methods=['POST'])
@cliente_auth_required
def bonifico():
    form = BonificoForm()
    url = url_for('cliente.conto_corrente', id=form.conto_corrente_id.data) if form.conto_corrente_id.data else url_for('cliente.dashboard')

    if form.validate_on_submit():
        # find conto corrente
        stmt = select(ContoCorrente).where(
            ContoCorrente.id == form.conto_corrente_id.data,
            (ContoCorrente.cliente1_id == session['cliente']['id']) | (
                ContoCorrente.cliente2_id == session['cliente']['id'])
        )
        conto_corrente = db.session.scalar(stmt)
        
        if not conto_corrente:
            flash('Conto corrente non trovato.', 'danger')
            return redirect(url)
        
        # max importo
        if form.importo.data > conto_corrente.saldo:
            flash('Saldo insufficiente.', 'danger')
            return redirect(url)
        
        if form.importo.data <= 0:
            flash('Importo non valido.', 'danger')
            return redirect(url)
        
        # check iban destinatario != iban mittente
        if form.iban_destinatario.data == conto_corrente.iban:
            flash('IBAN destinatario non valido.', 'danger')
            return redirect(url)
        
        # create the transazione interna
        transazione_interna = TransazioneInterna()
        transazione_interna.conto_corrente_id = form.conto_corrente_id.data
        
        db.session.add(transazione_interna)
        db.session.flush()
        db.session.refresh(transazione_interna)
        
        # create the transazione
        transazione = Transazione()
        transazione.importo = form.importo.data
        transazione.descrizione = f'Bonifico in favore di {form.iban_destinatario.data}' # type: ignore
        transazione.transazione_interna_id = transazione_interna.id
        transazione.entrata = False # type: ignore
        transazione.causale = form.causale.data
        
        db.session.add(transazione)

        # create the accredit transazione
        # check if destination iban is in conti correnti
        stmt = select(ContoCorrente).where(
            ContoCorrente.iban == form.iban_destinatario.data
        )
        conto_corrente_destinatario = db.session.scalar(stmt)
        
        if not conto_corrente_destinatario:
            t_ref = TransazioneEsterna()    
            t_ref.iban = form.iban_destinatario.data
        else:
            t_ref = TransazioneInterna()
            t_ref.conto_corrente_id = conto_corrente_destinatario.id
            
        db.session.add(t_ref)
        db.session.flush()
        db.session.refresh(t_ref)
            
        transazione_accredito = Transazione()
        transazione_accredito.importo = form.importo.data
        transazione_accredito.descrizione = f'Bonifico da {conto_corrente.iban}' # type: ignore
        transazione_accredito.transazione_id = transazione.id
        transazione_accredito.entrata = True # type: ignore
    
        if conto_corrente_destinatario:
            transazione_accredito.transazione_interna_id = t_ref.id
        else:
            transazione_accredito.transazione_esterna_id = t_ref.id
            
        db.session.add(transazione_accredito)
        db.session.flush()
        db.session.refresh(transazione_accredito)
        
        # update the ref id
        transazione.transazione_id = transazione_accredito.id
        db.session.add(transazione)
        
        # update the conto corrente
        conto_corrente.saldo -= form.importo.data
        if conto_corrente_destinatario:
            conto_corrente_destinatario.saldo += form.importo.data
            db.session.add(conto_corrente_destinatario)
            
        db.session.add(conto_corrente)
        
        try:
            db.session.commit()
            flash('Bonifico effettuato con successo.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error durante il bonifico: {e}', 'error')
            
    return redirect(url)

        
@client_page.route('/prestiti', methods=['GET', 'POST'])
@cliente_auth_required
def prestiti():
    form = PrestitoForm()
    
    # find conto correnti of current user
    conto_correnti = db.session.query(ContoCorrente).where(
        (ContoCorrente.cliente1_id == session['cliente']['id']) | (
            ContoCorrente.cliente2_id == session['cliente']['id'])
    ).all()
    form.conto_corrente_id.choices = [(c.id, c.iban) for c in conto_correnti]
    
    if form.validate_on_submit():
        # create the prestito
        prestito = Prestito()
        prestito.importo = form.importo.data
        prestito.cliente_id = session['cliente']['id']
        
        # check if selected conto corrente is owned by cliente
        if form.conto_corrente_id.data in [c.id for c in conto_correnti]:
            prestito.conto_corrente_id = form.conto_corrente_id.data
        else:
            flash("Conto corrente non valido", 'error')
            return redirect(url_for('cliente.prestiti'))

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

    return render_template('cliente/prestiti.html', prestito_form=form, prestiti=prestiti)


@client_page.route('/account', methods=['GET', 'POST'])
@cliente_auth_required
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

    return render_template('cliente/account.html', account_form=form)
