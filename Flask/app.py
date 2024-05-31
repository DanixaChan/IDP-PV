from flask import Flask, jsonify, request, send_from_directory, render_template
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# Funciones para obtener datos desde las APIs
def obtener_boletas_externas():
    """
    Obtiene los datos de las boletas de origen externo
    ---
    responses:
     200:
            description: Se obtiene las boletas de forma externa a partir de otro en>
    """
    response = requests.get(app.config['API_BOLETAS_URL'])
    if response.status_code == 200:
        return response.json()
    else:
        return []

def obtener_ordenes_despacho_externas():
    """
    Obtiene los datos de las ordenes de despacho de origen externo
    ---
    responses:
     200:
            description: Se obtiene las ordenes de despacho a partir de otro endpoint
    """
    response = requests.get(app.config['http://44.205.221.190:8000/despachos/'])
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
    response = requests.get(app.config['http://44.205.221.190:8000/despachos/'], timeout=10)
    if response.status_code == 200:
        datos = response.json()
        return jsonify(datos)
    else:
        return f'Error al obtener los datos de la instancia de EC2: {response.text}', 500

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
        id=boleta_data['id'],
        numero=boleta_data['numero'],
        fecha=boleta_data['fecha'],
        total=boleta_data['total']
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
    enduro_data = obtener_boletas_externas()
    
    # Obtener los datos de la API de despacho
    despacho_data = obtener_ordenes_despacho_externas()
    
    # Combinar los datos
    datos_combinados = {'enduro_data': enduro_data, 'despacho_data': despacho_data}
    
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
