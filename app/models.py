from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    """ Modelo de usuário """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Voo(db.Model):
    """ Modelo de voo """
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    mercado = db.Column(db.String(10), nullable=False)
    rpk = db.Column(db.Float, nullable=False)