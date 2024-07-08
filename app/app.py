from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv
import os

from db.user import find_user
from forms import LoginForm

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
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
    
    return render_template('auth/login.html', title='Login', form=form)