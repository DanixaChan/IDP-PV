from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from config import Config
from models import db, Boleta, Despacho
from flasgger import Swagger

# Configuración de la aplicación Flask
template_dir = os.path.abspath('../templates')
app = Flask(__name__, template_folder=template_dir, static_folder='../static')
app.config.from_object(Config)
db.init_app(app)  # Inicialización de SQLAlchemy
swagger = Swagger(app)  # Inicialización de Swagger para documentación

# Crear todas las tablas en la base de datos (solo en desarrollo)
with app.app_context():
    db.create_all()

# Funciones para obtener datos desde las APIs externas
def obtener_boletas_externas():
    """
    Obtiene los datos de las boletas desde la API externa
    ---
    responses:
     200:
            description: Datos de las boletas obtenidos correctamente
    """
    response = requests.get(app.config['http://54.159.228.5:8000/boletasVentasPosVentas/'])
    if response.status_code == 200:
        return response.json()
    else:
        return []

def obtener_ordenes_despacho_externas():
    """
    Obtiene los datos de las órdenes de despacho desde la API externa
    ---
    responses:
     200:
            description: Datos de las órdenes de despacho obtenidos correctamente
    """
    response = requests.get(app.config['http://44.205.221.190:8000/despachos/'])
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Funciones para almacenar datos en la base de datos
def almacenar_boletas_en_interna(boletas):
    """
    Almacena los datos de las boletas en la base de datos interna
    ---
    responses:
     200:
            description: Boletas almacenadas correctamente en la base de datos
    """
    for boleta in boletas:
        nueva_boleta = Boleta(
            numero_boleta=boleta['Numero_boleta'],
            fecha_emision=boleta['fecha_emision'],
            cliente=boleta['cliente'],
            items_boleta=boleta['Items_boleta'],
            total=boleta['Total'],
            estado=boleta['Estado']
        )
        db.session.add(nueva_boleta)
    db.session.commit()

def almacenar_ordenes_despacho_en_interna(ordenes):
    """
    Almacena los datos de las órdenes de despacho en la base de datos interna
    ---
    responses:
     200:
            description: Órdenes de despacho almacenadas correctamente en la base de datos
    """
    for orden in ordenes:
        nuevo_despacho = Despacho(
            fecha_despacho=orden['fecha_despacho'],
            patente_camion=orden['patente_camion'],
            intento=orden['intento'],
            entregado=orden['entregado'],
            id_compra=orden['id_compra'],
            direccion_compra=orden['direccion_compra'],
            valor_compra=orden['valor_compra']
        )
        db.session.add(nuevo_despacho)
    db.session.commit()

# Rutas de la aplicación

@app.route('/')
def index():
    """
    Ruta principal de la aplicación
    ---
    responses:
     200:
            description: Página principal de la aplicación
    """
    return render_template('index.html')

@app.route('/boletas', methods=['GET'])
def mostrar_boletas():
    """
    Muestra todas las boletas almacenadas en la base de datos
    ---
    responses:
     200:
            description: Muestra las boletas almacenadas
    """
    boletas = Boleta.query.all()
    return jsonify([boleta.to_dict() for boleta in boletas])

@app.route('/ordenes_despacho', methods=['GET'])
def mostrar_ordenes_despacho():
    """
    Muestra todas las órdenes de despacho almacenadas en la base de datos
    ---
    responses:
     200:
            description: Muestra las órdenes de despacho almacenadas
    """
    ordenes = Despacho.query.all()
    return jsonify([orden.to_dict() for orden in ordenes])

@app.route('/guardar_boleta', methods=['POST'])
def guardar_boleta():
    """
    Guarda una nueva boleta en la base de datos desde el cliente
    ---
    responses:
     200:
            description: Guarda una nueva boleta en la base de datos
    """
    boleta_data = request.json
    nueva_boleta = Boleta(
        numero_boleta=boleta_data['numero_boleta'],
        fecha_emision=boleta_data['fecha_emision'],
        cliente=boleta_data['cliente'],
        items_boleta=boleta_data['items_boleta'],
        total=boleta_data['total'],
        estado=boleta_data['estado']
    )
    db.session.add(nueva_boleta)
    db.session.commit()
    return jsonify({'message': 'Datos de boleta recibidos correctamente'})

@app.route('/sincronizar_boletas', methods=['GET'])
def sincronizar_boletas():
    """
    Sincroniza las boletas desde la API externa a la base de datos
    ---
    responses:
     200:
            description: Sincroniza las boletas con la base de datos
    """
    boletas = obtener_boletas_externas()
    almacenar_boletas_en_interna(boletas)
    return jsonify({'message': 'Boletas sincronizadas correctamente'})

@app.route('/sincronizar_ordenes_despacho', methods=['GET'])
def sincronizar_ordenes_despacho():
    """
    Sincroniza las órdenes de despacho desde la API externa a la base de datos
    ---
    responses:
     200:
            description: Sincroniza las órdenes de despacho con la base de datos
    """
    ordenes = obtener_ordenes_despacho_externas()
    almacenar_ordenes_despacho_en_interna(ordenes)
    return jsonify({'message': 'Órdenes de despacho sincronizadas correctamente'})

if __name__ == '__main__':
    app.run(debug=True)

