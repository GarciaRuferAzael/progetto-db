from flask import Blueprint, flash, redirect, render_template, request, url_for
from .forms import LoginForm


employee_page = Blueprint('employee', __name__, template_folder="templates/employee")

@employee_page.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            
            # user = find_user(email, password)
            # if user:
            #     flash('Login successful!', 'success')
            #     return redirect(url_for('index'))
            # else:
            #   flash('Invalid email or password', 'danger')
        
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html', login_form=login_form)
