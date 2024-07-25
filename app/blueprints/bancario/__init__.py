from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from db import Bancario
from .forms import LoginForm


bancario_page = Blueprint('bancario', __name__, template_folder="templates/bancario")

@bancario_page.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data

            cliente = Bancario.query.filter_by(email=email).first()

            if cliente:
                # check if the password is correct
                if cliente.verify_password(password):
                    flash('Login successful!', 'success')
                    session['bancario'] = cliente.serialize()
                    return redirect(url_for('bancario.dashboard'))

                flash('Invalid email or password', 'danger')
            else:
                flash('Invalid email or password', 'danger')

    return render_template('login.html', login_form=login_form)
