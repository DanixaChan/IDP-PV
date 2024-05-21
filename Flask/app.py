# app.py

from flask import Flask, render_template, send_from_directory, jsonify
import os
import requests
from config import Config
from models import db, Boleta, OrdenDespacho

template_dir = os.path.abspath('../templates')

app = Flask(__name__, template_folder=template_dir, static_folder='../static')
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/img/icono_emp.png')
def img():
    return send_from_directory(app.static_folder, 'icono_emp.png')

@app.route('/img/test-img-prod.jpg')
def img_prod():
    return send_from_directory(app.static_folder, 'test-img-prod.jpg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/b_boleta')
def gboleta():
    return render_template('b_boleta.html')

@app.route('/go_despacho')
def godespacho():
    return render_template('go_despacho.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

def obtener_boletas_externas():
    response = requests.get(app.config['API_BOLETAS_URL'])
    if response.status_code == 200:
        return response.json()
    else:
        return []

def obtener_ordenes_despacho_externas():
    response = requests.get(app.config['http://44.205.221.190:8000/despachos/'])
    if response.status_code == 200:
        return response.json()
    else:
        return []

def almacenar_boletas_en_interna(boletas):
    for boleta in boletas:
        nueva_boleta = Boleta(
            id=boleta['id'],
            numero=boleta['numero'],
            fecha=boleta['fecha'],
            total=boleta['total']
        )
        db.session.add(nueva_boleta)
    db.session.commit()

def almacenar_ordenes_despacho_en_interna(ordenes):
    for orden in ordenes:
        nueva_orden = OrdenDespacho(
            id=orden['id'],
            numero=orden['numero'],
            fecha=orden['fecha'],
            estado=orden['estado']
        )
        db.session.add(nueva_orden)
    db.session.commit()

@app.route('/sincronizar_boletas')
def sincronizar_boletas():
    boletas = obtener_boletas_externas()
    almacenar_boletas_en_interna(boletas)
    return jsonify({'message': 'Boletas sincronizadas correctamente'})

@app.route('/sincronizar_ordenes_despacho')
def sincronizar_ordenes_despacho():
    ordenes = obtener_ordenes_despacho_externas()
    almacenar_ordenes_despacho_en_interna(ordenes)
    return jsonify({'message': 'Órdenes de despacho sincronizadas correctamente'})

@app.route('/boletas')
def mostrar_boletas():
    boletas = Boleta.query.all()
    return render_template('boletas.html', boletas=boletas)

@app.route('/ordenes_despacho')
def mostrar_ordenes_despacho():
    ordenes = OrdenDespacho.query.all()
    return render_template('ordenes_despacho.html', ordenes=ordenes)

if __name__ == '__main__':
    app.run(host=None, debug=True)
