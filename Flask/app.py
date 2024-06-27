from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from config import Config
from models import db, Boleta, Despacho
from flasgger import Swagger
from datetime import datetime

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
    """
    try:
        response = requests.get('http://54.159.228.5:8000/boletasVentasPosVentas/')
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa

        return response.json()

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error al obtener datos de la API externa de boletas: {e}")
        return []

def almacenar_boletas_en_interna(boletas):
    """
    Almacena los datos de las boletas en la base de datos interna
    """
    try:
        for boleta in boletas:
            nueva_boleta = Boleta(
                numero_boleta=boleta['numero_boleta'],
                fecha_emision=datetime.strptime(boleta['fecha_emision'], '%Y-%m-%d').date(),
                cliente=boleta['cliente'],
                items_boleta=boleta['items_boleta'],
                total=boleta['total'],
                estado=boleta['estado']
            )
            db.session.add(nueva_boleta)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al almacenar boletas en la base de datos: {e}")

def obtener_ordenes_despacho_externas():
    """
    Obtiene los datos de las órdenes de despacho desde la API externa
    """
    try:
        response = requests.get('http://44.205.221.190:8000/despachos/')
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa

        return response.json()

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error al obtener datos de la API externa de órdenes de despacho: {e}")
        return []

def almacenar_ordenes_despacho_en_interna(ordenes):
    """
    Almacena los datos de las órdenes de despacho en la base de datos interna
    """
    try:
        for orden in ordenes:
            nuevo_despacho = Despacho(
                fecha_despacho=datetime.strptime(orden['fecha_despacho'], '%Y-%m-%d').date(),
                patente_camion=orden['patente_camion'],
                intento=orden['intento'],
                entregado=orden['entregado'],
                id_compra=orden['id_compra'],
                direccion_compra=orden['direccion_compra'],
                valor_compra=orden['valor_compra']
            )
            db.session.add(nuevo_despacho)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al almacenar órdenes de despacho en la base de datos: {e}")

# Rutas de la aplicación

@app.route('/')
def index():
    """
    Ruta principal de la aplicación
    """
    return render_template('index.html')

@app.route('/boletas', methods=['GET'])
def mostrar_boletas():
    """
    Muestra todas las boletas almacenadas en la base de datos
    """
    try:
        boletas = Boleta.query.all()
        return jsonify([boleta.to_dict() for boleta in boletas])

    except Exception as e:
        app.logger.error(f"Error al recuperar boletas de la base de datos: {e}")
        return jsonify({'error': 'Error al recuperar boletas de la base de datos'}), 500

@app.route('/ordenes_despacho', methods=['GET'])
def mostrar_ordenes_despacho():
    """
    Muestra todas las órdenes de despacho almacenadas en la base de datos
    """
    try:
        ordenes = Despacho.query.all()
        return jsonify([orden.to_dict() for orden in ordenes])

    except Exception as e:
        app.logger.error(f"Error al recuperar órdenes de despacho de la base de datos: {e}")
        return jsonify({'error': 'Error al recuperar órdenes de despacho de la base de datos'}), 500

@app.route('/obtener_datos_ec2_boletas', methods=['GET'])
def obtener_datos_ec2_boletas():
    """
    Obtiene los datos de las boletas desde la API externa y los almacena en la base de datos
    """
    try:
        boletas = obtener_boletas_externas()
        almacenar_boletas_en_interna(boletas)
        return jsonify({'message': 'Datos de boletas obtenidos y almacenados correctamente'}), 200

    except Exception as e:
        app.logger.error(f"Error en la obtención y almacenamiento de boletas: {e}")
        return jsonify({'error': 'Error en la obtención y almacenamiento de boletas'}), 500

@app.route('/obtener_datos_ec2_ordenes_despacho', methods=['GET'])
def obtener_datos_ec2_ordenes_despacho():
    """
    Obtiene los datos de las órdenes de despacho desde la API externa y las almacena en la base de datos
    """
    try:
        ordenes = obtener_ordenes_despacho_externas()
        almacenar_ordenes_despacho_en_interna(ordenes)
        return jsonify({'message': 'Datos de órdenes de despacho obtenidos y almacenados correctamente'}), 200

    except Exception as e:
        app.logger.error(f"Error en la obtención y almacenamiento de órdenes de despacho: {e}")
        return jsonify({'error': 'Error en la obtención y almacenamiento de órdenes de despacho'}), 500

if __name__ == '__main__':
    app.run(debug=True)

