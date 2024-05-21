#models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Boleta(db.Model):
    __tablename__ = 'boletas'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)

class OrdenDespacho(db.Model):
    __tablename__ = 'ordenes_despacho'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
