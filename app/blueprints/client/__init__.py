from datetime import date, datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from sqlalchemy import select
from db import db
from db.client import Client
from .forms import LoginForm, AccountForm


client_page = Blueprint('client', __name__, template_folder="templates/client")

@client_page.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            
            stmt = select(Client).where(Client.email == email)
            client = db.session.scalar(stmt)
        
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
def logout():
    session.pop('client', None)
    return redirect(url_for('client.login'))


@client_page.route('/dashboard', methods=['GET'])
def dashboard():
    # Mock data for the client dashboard
    conto_corrente_info = [
        {'id': 1, 'saldo_conto': 'xxx', 'entrate_uscite_mese': 'xxx'},
        {'id': 2, 'saldo_conto': 'xxx', 'entrate_uscite_mese': 'xxx'}
    ]
    return render_template('dashboard.html', conti=conto_corrente_info)

@client_page.route('/prestiti', methods=['GET'])
def prestiti():
    return render_template('prestiti.html')

@client_page.route('/carte', methods=['GET'])
def carte():
    return render_template('carte.html')

@client_page.route('/azioni', methods=['GET'])
def azioni():
    return render_template('azioni.html')

@client_page.route('/account', methods=['GET', 'POST'])
def account():
    form = AccountForm()
    
    # transform date format
    data_nascita = datetime.strptime(session["client"]["data_nascita"], '%a, %d %b %Y %H:%M:%S %Z')
    data_nascita = date(data_nascita.year, data_nascita.month, data_nascita.day)
    session["client"]["data_nascita"] = data_nascita
    
    if request.method == 'POST':
        if form.validate_on_submit():
            id = session["client"]["id"]
            
            # find client
            stmt = select(Client).where(Client.id == id)
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