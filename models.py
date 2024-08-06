from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Baza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(150), nullable=False)
    contact_details = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(50), nullable=True)

class BazaGold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(150), nullable=False)
    contact_details = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(50), nullable=True)

class BazaCold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(150), nullable=False)
    contact_details = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(50), nullable=True)
