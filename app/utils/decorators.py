from functools import wraps
from flask import session, redirect, url_for

def client_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('client'):
            return redirect(url_for('client.login'))
        return f(*args, **kwargs)
    return decorated_function

def client_unauth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('client'):
            return redirect(url_for('client.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def employee_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('employee'):
            return redirect(url_for('employee.login'))
        return f(*args, **kwargs)
    return decorated_function

def director_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('director'):
            return redirect(url_for('director.login'))
        return f(*args, **kwargs)
    return decorated_function