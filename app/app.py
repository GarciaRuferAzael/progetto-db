from flask import Flask, render_template
import os

from db import db

from blueprints.cliente import client_page
from blueprints.bancario import bancario_page
from blueprints.direttore import director_page

app = Flask(__name__)

if app.debug:
    from dotenv import load_dotenv
    load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")

# check if path exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

db.init_app(app)

app.register_blueprint(client_page, url_prefix="/cliente/")
app.register_blueprint(bancario_page, url_prefix="/bancario/")
app.register_blueprint(director_page, url_prefix="/direttore/")


@app.route("/")
def index():
    return render_template('index.html')


def get_routes_for(name: str):
    client_routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith(f'{name}.') and rule.endpoint.split('.')[1] not in ['login', 'logout'] and rule.methods and "GET" in rule.methods:
            client_routes.append((rule.endpoint, rule.rule))
    return client_routes


@app.context_processor
def client_routes():
    routes = get_routes_for('cliente')
    return dict(client_routes=routes)


@app.context_processor
def bancario_routes():
    routes = get_routes_for('bancario')
    return dict(bancario_routes=routes)


@app.context_processor
def director_routes():
    routes = get_routes_for('direttore')
    return dict(director_routes=routes)
