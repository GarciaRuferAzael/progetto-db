from flask import Blueprint, flash, redirect, render_template, request, url_for
from forms import LoginForm


director_page = Blueprint('director', __name__, template_folder="templates/director")

@director_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            # user = find_user(email, password)
            # if user:
            #     flash('Login successful!', 'success')
            #     return redirect(url_for('index'))
            # else:
            #   flash('Invalid email or password', 'danger')
        
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)
