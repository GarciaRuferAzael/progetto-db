from flask import Flask, render_template
import os

from db import db

from blueprints.cliente import client_page
from blueprints.bancario import bancario_page
from blueprints.direttore import direttore_page

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
app.register_blueprint(direttore_page, url_prefix="/direttore/")


@app.route("/")
def index():
    return render_template('index.html')


def get_routes_for(name: str, routes_list: list[str]):
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith(f'{name}.') and rule.endpoint.split('.')[1] in routes_list:
            routes.append((rule.endpoint, rule.rule))
    return routes


@app.context_processor
def cliente_routes():
    routes = get_routes_for('cliente', ["dashboard", "prestiti", "account"])
    return dict(cliente_routes=routes)


@app.context_processor
def bancario_routes():
    routes = get_routes_for('bancario', ["dashboard", "richieste", "polizze", "account"])
    return dict(bancario_routes=routes)


@app.context_processor
def direttore_routes():
    routes = get_routes_for('direttore', ["dashboard", "richieste", "account"])
    return dict(direttore_routes=routes)
