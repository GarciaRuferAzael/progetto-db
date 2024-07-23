from flask import Flask, render_template
import os

from db import db

from blueprints.client import client_page
from blueprints.employee import employee_page
from blueprints.director import director_page

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
app.register_blueprint(employee_page, url_prefix="/bancario/")
app.register_blueprint(director_page, url_prefix="/direttore/")


@app.route("/")
def index():
    return render_template('index.html')


def get_routes_for(name: str):
    client_routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith(f'{name}.') and rule.endpoint.split('.')[1] not in ['login', 'logout']:
            client_routes.append((rule.endpoint, rule.rule))
    return client_routes


@app.context_processor
def client_routes():
    routes = get_routes_for('client')
    return dict(client_routes=routes)


@app.context_processor
def employee_routes():
    routes = get_routes_for('employee')
    return dict(employee_routes=routes)


@app.context_processor
def director_routes():
    routes = get_routes_for('director')
    return dict(director_routes=routes)
