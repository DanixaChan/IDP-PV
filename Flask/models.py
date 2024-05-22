#models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Boleta(db.Model):
    __tablename__ = 'boletas'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)

class Despacho(db.Model):
    __tablename__ = 'despachos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_despacho = db.Column(db.String(50), nullable=False)
    patente_camion = db.Column(db.String(50), nullable=False)
    intento = db.Column(db.Integer, nullable=False)
    entregado = db.Column(db.Boolean, nullable=False)
    id_compra = db.Column(db.String(50), nullable=False)
    direccion_compra = db.Column(db.String(200), nullable=False)
    valor_compra = db.Column(db.Float, nullable=False)
