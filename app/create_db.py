from dotenv import load_dotenv
load_dotenv()

from app import app
from db import db

with app.app_context():
    db.create_all()
    db.session.commit()