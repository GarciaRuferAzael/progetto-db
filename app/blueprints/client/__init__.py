from flask import Blueprint, flash, redirect, render_template, request, url_for
from db.user import find_user
from forms import LoginForm


client_page = Blueprint('client', __name__, template_folder="templates/client")

@client_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            user = find_user(email, password)
            if user:
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password', 'danger')
        
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)


@client_page.route('/dashboard', methods=['GET'])
def dashboard_cliente():
    # Mock data for the client dashboard
    conto_corrente_info = [
        {'id': 1, 'saldo_conto': 'xxx', 'entrate_uscite_mese': 'xxx'},
        {'id': 2, 'saldo_conto': 'xxx', 'entrate_uscite_mese': 'xxx'},
        {'id': 3, 'saldo_conto': 'xxx', 'entrate_uscite_mese': 'xxx'}
    ]
    return render_template('dashboard.html', conti=conto_corrente_info)