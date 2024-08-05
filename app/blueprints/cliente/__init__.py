from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from datetime import date, datetime
from sqlalchemy import select
from db import CartaPrepagata, ContoCorrente, RichiestaCartaPrepagata, RichiestaContoCorrente, Transazione, TransazioneEsterna, TransazioneInterna, db
from db import Prestito, Cliente, Garanzia
from db.query import get_transazioni_by_conto_corrente_id
from utils.decorators import cliente_auth_required, cliente_unauth_required
from utils.storage import save_file
from .forms import BonificoForm, LoginForm, AccountForm, PrestitoForm, RicaricaCartaForm


cliente_page = Blueprint('cliente', __name__, template_folder="templates")


@cliente_page.route('/login', methods=['GET', 'POST'])
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


@cliente_page.route('/logout', methods=['GET'])
@cliente_auth_required
def logout():
    session.pop('cliente', None)
    return redirect(url_for('cliente.login'))


@cliente_page.route('/dashboard', methods=['GET'])
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


@cliente_page.route('/richiesta_conto_corrente', methods=['POST'])
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


@cliente_page.route('/add_user_conto_corrente', methods=['POST'])
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


@cliente_page.route('/conto_corrente/<int:id>', methods=['GET'])
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
        {"data": t.data.strftime('%Y-%m-%d %H:%M:%S'),
         "importo": t.importo, "entrata": t.entrata}
        for t in transazioni
    ]

    return render_template(
        'cliente/conto_corrente.html',
        conto_corrente=conto_corrente,
        transazioni=transazioni,
        t_list=t_list,
        bonifico_form=form
    )


@cliente_page.route('/bonifico', methods=['POST'])
@cliente_auth_required
def bonifico():
    form = BonificoForm()
    url = url_for('cliente.conto_corrente',
                  id=form.conto_corrente_id.data) if form.conto_corrente_id.data else url_for('cliente.dashboard')

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
        transazione.descrizione = f'Bonifico in favore di {form.iban_destinatario.data}'  #type: ignore
        transazione.transazione_interna_id = transazione_interna.id
        transazione.entrata = False  # type: ignore
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
        transazione_accredito.entrata = True  # type: ignore

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


@cliente_page.route('/richiesta_carta_prepagata', methods=['POST'])
@cliente_auth_required
def richiesta_carta_prepagata():
    cliente = db.session.query(Cliente).where(
        Cliente.id == session["cliente"]["id"]).first()
    if not cliente:
        flash("Cliente non trovato", "error")
        
        return redirect(url_for('cliente.logout'))
    
    # create RichiestaCartaPrepagata
    richiesta = RichiestaCartaPrepagata()
    richiesta.cliente_id = cliente.id
    db.session.add(richiesta)
    
    try:
        db.session.commit()
        flash('Richiesta inviata con successo.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error durante l\'invio della richiesta: {e}', 'error')
        
    return redirect(url_for('cliente.carte'))


@cliente_page.route('/disabilita_carta', methods=['POST'])
@cliente_auth_required
def disabilita_carta():
    cliente = db.session.query(Cliente).where(
        Cliente.id == session["cliente"]["id"]).first()
    
    if not cliente:
        flash("Cliente non trovato", "error")
        return redirect(url_for('cliente.logout'))
        
    carta_id = request.form.get('carta_id', type=int)
    carta = db.session.query(CartaPrepagata).where(
        CartaPrepagata.id == carta_id,
        CartaPrepagata.cliente_id == cliente.id
    ).first()
    
    if not carta:
        flash("Carta non trovata", "error")
        return redirect(url_for('cliente.carte'))
    
    carta.disabilitata = bool(request.form.get('disabilita', type=int)) # type: ignore
    db.session.add(carta)
    
    try:
        db.session.commit()
        flash('Carta aggiornata con successo.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error durante l\'aggiornamento: {e}', 'error')
        
    return redirect(url_for('cliente.carte'))

@cliente_page.route('/richieste', methods=['GET'])
@cliente_auth_required
def ricarica_carta():
    return redirect(url_for('cliente.carte'))

@cliente_page.route('/carte', methods=['GET'])
@cliente_auth_required
def carte():
    form = RicaricaCartaForm()
    
    cliente = db.session.query(Cliente).where(
        Cliente.id == session["cliente"]["id"]).first()
    if not cliente:
        flash("Cliente non trovato", "error")
        return redirect(url_for('cliente.logout'))
    
    form.conto_corrente_id.choices = [(c.id, c.iban) for c in cliente.conti_correnti]

    carte_prepagate = cliente.carte_prepagate
    richieste_in_attesa = db.session.query(RichiestaCartaPrepagata).where(
        RichiestaCartaPrepagata.cliente_id == cliente.id,
        RichiestaCartaPrepagata.accettata == None
    ).count()

    return render_template(
        'cliente/carte.html',
        carte_prepagate=carte_prepagate,
        richieste_in_attesa=richieste_in_attesa,
        ricarica_form=form
    )


@cliente_page.route('/ricarica_carta_prepagata', methods=['POST'])
@cliente_auth_required
def ricarica_carta_prepagata():
    form = RicaricaCartaForm()
    
    cliente = db.session.query(Cliente).where(
        Cliente.id == session["cliente"]["id"]).first()
    if not cliente:
        flash("Cliente non trovato", "error")
        return redirect(url_for('cliente.logout'))
    
    form.conto_corrente_id.choices = [(c.id, c.iban) for c in cliente.conti_correnti]

    if not form.validate_on_submit():
        flash("Dati non validi", "error")
        return redirect(url_for('cliente.carte'))
    
    conto_corrente = db.session.query(ContoCorrente).where(
        ContoCorrente.id == form.conto_corrente_id.data
    ).first()
    
    carta_id = form.carta_prepagata_id.data
    carta = db.session.query(CartaPrepagata).where(
        CartaPrepagata.id == carta_id,
        CartaPrepagata.cliente_id == cliente.id
    ).first()
    if not carta:
        flash("Carta non trovata", "error")
        return redirect(url_for('cliente.carte'))
        
    importo = form.importo.data
    if not importo or importo <= 0:
        flash("Importo non valido", "error")
        return redirect(url_for('cliente.carte'))
    if importo > conto_corrente.saldo: # type: ignore
        flash("Saldo insufficiente", "error")
        return redirect(url_for('cliente.carte'))
    
    # create the transazione addebito conto
    tid = TransazioneInterna()
    tid.conto_corrente_id = conto_corrente.id # type: ignore
    
    db.session.add(tid)
    db.session.flush()
    db.session.refresh(tid)
    
    t = Transazione()
    t.importo = importo # type: ignore
    t.descrizione = f'Ricarica carta prepagata {carta.numero}' # type: ignore
    t.transazione_interna_id = tid.id
    t.entrata = False # type: ignore
    
    db.session.add(t)
    db.session.flush()
    db.session.refresh(t)
    
    # create the transazione accredito carta
    tic = TransazioneInterna()
    tic.carta_prepagata_id = carta.id
    
    db.session.add(tic)
    db.session.flush()
    db.session.refresh(tic)
    
    t2 = Transazione()
    t2.importo = importo # type: ignore
    t2.descrizione = f'Ricarica da {conto_corrente.iban}' # type: ignore
    t2.transazione_interna_id = tic.id
    t2.entrata = True # type: ignore
    t2.transazione_id = t.id
    
    db.session.add(t2)
    db.session.flush()
    db.session.refresh(t2)
    
    t.transazione_id = t2.id
    db.session.add(t)
    
    carta.saldo = carta.saldo + importo
    db.session.add(carta)
    
    conto_corrente.saldo = conto_corrente.saldo - importo # type: ignore
    db.session.add(conto_corrente)
    
    try:
        db.session.commit()
        flash('Ricarica effettuata con successo.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error durante la ricarica: {e}', 'error')
        
    return redirect(url_for('cliente.carte'))


@cliente_page.route('/prestiti', methods=['GET', 'POST'])
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


@cliente_page.route('/account', methods=['GET', 'POST'])
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
