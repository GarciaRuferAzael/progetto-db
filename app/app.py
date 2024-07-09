from flask import Flask, render_template
from dotenv import load_dotenv
import os

from blueprints.client import client_page
from blueprints.employee import employee_page
from blueprints.director import director_page

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(client_page, url_prefix="/cliente/")
app.register_blueprint(employee_page, url_prefix="/bancario/")
app.register_blueprint(director_page, url_prefix="/direttore/")

@app.route("/")
def index():
    return render_template('index.html')