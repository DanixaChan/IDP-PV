from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Boleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'fecha': self.fecha,
            'total': self.total
        }

class Despacho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_despacho = db.Column(db.Date, nullable=False)
    patente_camion = db.Column(db.String(50), nullable=False)
    intento = db.Column(db.Integer, nullable=False)
    entregado = db.Column(db.Boolean, nullable=False)
    id_compra = db.Column(db.String(50), nullable=False)
    direccion_compra = db.Column(db.String(100), nullable=False)
    valor_compra = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'fecha_despacho': self.fecha_despacho,
            'patente_camion': self.patente_camion,
            'intento': self.intento,
            'entregado': self.entregado,
            'id_compra': self.id_compra,
            'direccion_compra': self.direccion_compra,
            'valor_compra': self.valor_compra
        }
