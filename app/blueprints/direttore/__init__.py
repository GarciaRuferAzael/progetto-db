from datetime import date, datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import select

from db import db, Direttore
from db.query import get_conti_correnti_by_direttore_id
from utils.decorators import direttore_auth_required, direttore_unauth_required
from .forms import AccountForm, LoginForm


director_page = Blueprint('direttore', __name__, template_folder="templates")

@director_page.route('/login', methods=['GET', 'POST'])
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

@director_page.route('/logout', methods=['GET'])
@direttore_auth_required
def logout():
    session.pop('direttore', None)
    return redirect(url_for('direttore.login'))

@director_page.route('/dashboard', methods=['GET'])
@direttore_auth_required
def dashboard():
    stmt = select(Direttore).where(Direttore.id == session["direttore"]["id"])
    direttore = db.session.scalar(stmt)
    
    if not direttore:
        return redirect(url_for('direttore.logout'))
    
    conti_correnti = get_conti_correnti_by_direttore_id(session["direttore"]["id"])
    filiale = direttore.filiale
    
    return render_template('direttore/dashboard.html', conti_correnti=conti_correnti, filiale=filiale)

@director_page.route('/account', methods=['GET', 'POST'])
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
    
    return render_template('bancario/account.html', account_form=form)