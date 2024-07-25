from functools import wraps
from flask import session, redirect, url_for

def cliente_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('cliente'):
            return redirect(url_for('cliente.login'))
        return f(*args, **kwargs)
    return decorated_function

def cliente_unauth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('cliente'):
            return redirect(url_for('cliente.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def bancario_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('bancario'):
            return redirect(url_for('bancario.login'))
        return f(*args, **kwargs)
    return decorated_function

def bancario_unauth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('bancario'):
            return redirect(url_for('bancario.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def direttore_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('direttore'):
            return redirect(url_for('direttore.login'))
        return f(*args, **kwargs)
    return decorated_function

def direttore_unauth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('direttore'):
            return redirect(url_for('direttore.dashboard'))
        return f(*args, **kwargs)
    return decorated_function