# app.py
import logging
from flask import Flask, jsonify, request, send_from_directory, render_template, url_for, flash, redirect
import os
import requests
from config import Config
from models import db, Boleta, Despacho
from flasgger import Swagger

# Configuración de la aplicación Flask
template_dir = os.path.abspath('../templates')
app = Flask(__name__, template_folder=template_dir, static_folder='../static')
template_dir = "templates"
app.config.from_object(Config)
app.secret_key = 'b5ef12e40e6bfe40350717229ceacf007a07f37e423f1cbd'  # Necesario para usar flash messages
db.init_app(app)
swagger = Swagger(app)

# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()

@app.route('/datos_json')
def ver_datos_json():
    """
    Renderiza una plantilla HTML con datos JSON
    ---
    responses:
     200:
            description: Plantilla HTML con datos JSON
    """
    return render_template('datos_json.html')

# Rutas para servir imágenes
@app.route('/img/icono_emp.png')
def img():
    return send_from_directory(app.static_folder, 'icono_emp.png')

@app.route('/img/test-img-prod.jpg')
def img_prod():
    return send_from_directory(app.static_folder, 'test-img-prod.jpg')

# Rutas para las diferentes páginas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/b_boleta')
def gboleta():
    return render_template('b_boleta.html')

@app.route('/go_despacho')
def godespacho():
    return render_template('go_despacho.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwb3N0dmVudGEiOiJ0b2tlbl9wb3N0dmVudGEifQ.WzZv3qmDOwup9c_n0mF-wfS6cS_whTGrpqhfDXIy-3g'

        data = {
            'username': username,
            'password': password,
            'token': token
        }

        response = requests.post('https://qic534o8o0.execute-api.us-east-1.amazonaws.com/validacionUsuarios/', json=data)

        if response.status_code == 200 and response.json().get('valid', False):
            flash('Login exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login fallido, por favor verifica tus credenciales', 'danger')

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# Ruta para mostrar la página de devolución
@app.route('/devolucion/<numero_boleta>', methods=['GET'])
def devolucion(numero_boleta):
    # Busca la boleta por el ID
    boleta = Boleta.query.filter_by(numero_boleta=numero_boleta).first()
    print("BOLETA DETECTADA")
    print(boleta, numero_boleta)
    if not boleta:
        return jsonify({'message': 'Boleta no encontrada'}), 404
    
    # Renderiza la plantilla 'devolucion.html' pasando los datos necesarios
    return render_template('devolucion.html', boleta=boleta.to_dict(), numero_boleta=numero_boleta)

@app.route('/procesar_devolucion', methods=['POST'])
def procesar_devolucion():
    data = request.json
    items_boleta = data.get('items_boleta')
    print("items data: ", items_boleta)

    # Buscar la boleta por items_boleta
    boleta = Boleta.query.filter_by(items_boleta=items_boleta).first()
    print("Items_boleta= ",boleta)

    if not boleta:
        return jsonify({'message': 'Boleta no encontrada'}), 404

    # Buscar la entrada de Stock correspondiente (asumo que tienes alguna clave de relación entre Boleta y Stock)
    entrada_stock = Stock.query.filter_by(nombre_producto=boleta.items_boleta).first()

    if not entrada_stock:
        return jsonify({'message': 'Entrada de Stock no encontrada para la boleta'}), 404

    # Actualizar la cantidad_producto
    nueva_cantidad = entrada_stock.cantidad_producto + 1
    entrada_stock.cantidad_producto = nueva_cantidad

    # Commit a la base de datos
    db.session.commit()

    return jsonify({
        'message': f'Se ha aumentado la cantidad_producto para la boleta con id {boleta.id}'
    }), 200

# Funciones para obtener datos desde las APIs
def obtener_boletas_externas():
    """
    Obtiene los datos de las boletas de origen externo
    ---
    responses:
     200:
            description: Se obtiene las boletas a partir de otro endpoint
    """
    response = requests.get(app.config['API_BOLETAS_URL'])
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({'error': 'No se pudo obtener la información de la API externa'}), response.status_code

def obtener_ordenes_despacho_externas():
    """
    Obtiene los datos de las ordenes de despacho de origen externo
    ---
    responses:
     200:
            description: Se obtiene las ordenes de despacho a partir de otro endpoint
    """
    response = requests.get(app.config['API_DESPACHO_URL'])
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Funciones para almacenar los datos en la base de datos
def almacenar_boletas_en_interna(boletas):
    """
    Almacena las boletas en BD
    ---
    responses:
     200:
            description: Se almacena las boletas obtenidas hacia la BD
    """
    try:
        with db.session.no_autoflush:
            for boleta in boletas:
                # No se verifica la existencia previa, se permite duplicados
                items_boleta = boleta['Items_boleta']
                if len(items_boleta) > 500:  # Ajustar el valor según el tamaño permitido
                    items_boleta = items_boleta[:500]
                
                nueva_boleta = Boleta(
                    numero_boleta=boleta['Numero_boleta'],
                    fecha_emision=boleta['Fecha_emision'],
                    cliente=boleta['Cliente'],
                    items_boleta=items_boleta,
                    total=boleta['Total'],
                    estado=boleta['Estado']
                )
                db.session.add(nueva_boleta)
            db.session.commit()
        logging.info("Todas las boletas han sido almacenadas exitosamente")
    except Exception as e:
        logging.error(f"Error al almacenar las boletas: {e}")
        db.session.rollback()

def almacenar_ordenes_despacho_en_interna(ordenes):
    """
    Almacena las ordenes de despacho en BD
    ---
    responses:
     200:
            description: Se almacena las boletas obtenidas hacia la BD
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

# Rutas para sincronizar los datos con la base de datos
@app.route('/sincronizar_boletas')
def sincronizar_boletas():
    """
    Sincronizacion de boletas a BD
    ---
    responses:
     200:
            description: Sincroniza las boletas con la BD
    """
    boletas = obtener_boletas_externas()
    almacenar_boletas_en_interna(boletas)
    return jsonify({'message': 'Boletas sincronizadas correctamente'})

@app.route('/sincronizar_ordenes_despacho')
def sincronizar_ordenes_despacho():
    """
    Sincronizacion de ordenes de despacho a BD
    ---
    responses:
     200:
            description: Sincroniza las ordenes de despacho con la BD
    """
    ordenes = obtener_ordenes_despacho_externas()
    almacenar_ordenes_despacho_en_interna(ordenes)
    return jsonify({'message': 'Órdenes de despacho sincronizadas correctamente'})

# Rutas para mostrar los datos almacenados
@app.route('/boletas')
def mostrar_boletas():
    """
    Visualiza los datos de las boletas almacenadas
    ---
    responses:
     200:
            description: Permite mostrar los datos de las boletas almacenadas
    """
    boletas = Boleta.query.all()
    return render_template('boletas.html', boletas=boletas)

@app.route('/ordenes_despacho')
def mostrar_ordenes_despacho():
    """
     Visualiza los datos de las ordenes de despacho almacenadas
    ---
    responses:
     200:
            description: Permite mostrar los datos de las ordenes de despacho almace>
    """
    ordenes = Despacho.query.all()
    return render_template('ordenes_despacho.html', ordenes=ordenes)

# Ruta para obtener los datos desde la instancia de EC2
@app.route('/obtener_datos_ec2')
def obtener_datos_ec2():
    """
     Visualiza los datos que se reciben desde el endpoint de despacho
    ---
    responses:
     200:
            description: Permite mostrar los datos de las ordenes de despacho encont>
    """
    response = requests.get(app.config['API_DESPACHOS_URL'], timeout=10)
    if response.status_code == 200:
        datos = response.json()
        return jsonify(datos)
    else:
        return f'Error al obtener los datos de la instancia de EC2: {response.text}', 500

# Ruta para obtener los datos desde la instancia de EC2 de Contabilidad
@app.route('/obtener_datos_ec2_boletas')
def obtener_datos_ec2_boletas():
    """
     Visualiza los datos que se reciben desde el endpoint de Contabilidad
    ---
    responses:
     200:
            description: Permite mostrar los datos de las boletas generadas en contabilidad encont>
    """
    response = requests.get(app.config['API_BOLETAS_URL'], timeout=10)
    if response.status_code == 200:
        datos = response.json()
        return jsonify(datos)
    else:
        return f'Error al obtener los datos de la instancia de EC2 de boletas: {response.text}', 500

# Nueva ruta para recibir los datos de boleta desde el cliente
@app.route('/guardar_boleta', methods=['POST'])
def guardar_boleta():
    """
     Ruta para guardar datos de las boletas desde el cliente
    ---
    responses:
     200:
            description: Permite acceder a la recepción de datos de boleta desde cli>
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

# Función para obtener y combinar los datos de "enduro" y la API de despacho
def obtener_y_combinar_datos():
    """
     Obtiene y combina los datos de las boletas con las ordenes de despacho
    ---
    responses:
     200:
            description: Primero obtiene los datos de las boletas y ordenes de despa>
    """
    # Obtener los datos de "enduro"
    boleta_data = obtener_boletas_externas()
    
    # Obtener los datos de la API de despacho
    despacho_data = obtener_ordenes_despacho_externas()
    
    # Combinar los datos
    datos_combinados = {'boleta_data': boleta_data, 'despacho_data': despacho_data}
    
    return datos_combinados

# Ruta para obtener los datos combinados
@app.route('/datos_combinados', methods=['GET'])
def datos_combinados():
    """
     Obtiene datos combinados
    ---
    responses:
     200:
            description: Recibe los datos combinados a partir de la función 'obtener>
    """
    # Obtener y devolver los datos combinados
    datos_combinados = obtener_y_combinar_datos()
    return jsonify(datos_combinados)

# Endpoint para obtener todos los datos en formato JSON
@app.route('/todos_los_datos', methods=['GET'])
def todos_los_datos():
    """
     Endpoint con todos los datos
    ---
    responses:
     200:
            description: Endpoint que contiene todos los datos en formato JSON
    """
    boletas = Boleta.query.all()
    despachos = Despacho.query.all()
    boletas_data = [boleta.to_dict() for boleta in boletas]
    despachos_data = [despacho.to_dict() for despacho in despachos]
    return jsonify({'boletas': boletas_data, 'despachos': despachos_data})

def obtener_boleta_por_numero(numero_boleta):
    # if numero_boleta == '1':
    #     return {
    #         'numero_boleta': '1',
    #         'fecha_emision': '2024-05-18',
    #         'cliente': 'Juan Pérez',
    #         'total': '1000'
    #     }
    # return None
    boletas = obtener_boletas_externas()
    for boleta in boletas:
        print(boleta)
        if boleta['Numero_boleta'] == numero_boleta:
            app.logger.info(f"boleta: {numero_boleta}")
            print("ENCONTRADO")
            return boleta
    return None

@app.route("/devolucion/<string:numero_boleta>")
def devolucion_boleta_id(numero_boleta):
    try:
        app.logger.info(f"Recibido numero_boleta: {numero_boleta}")
        boleta = obtener_boleta_por_numero(numero_boleta)
        app.logger.info(f"Boleta obtenida: {boleta}")
        if boleta is None:
            app.logger.error("Error al obtener las boletas de la API externa")
            return "Error al obtener las boletas de la API externa", 500

        app.logger.info(f"Boleta obtenida: {boleta}")
        return render_template('devolucion.html', boleta=boleta)
    except Exception as e:
        app.logger.error(f"Error en la función devolucion_boleta_id: {str(e)} de boleta {numero_boleta}")
        return f"Error en la función devolucion_boleta_id: {str(e)}, de boleta: {numero_boleta} tipo: {type(numero_boleta)}", 500

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
