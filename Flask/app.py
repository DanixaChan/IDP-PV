from flask import Flask, render_template, send_from_directory
import os

template_dir = os.path.abspath('../templates')

app = Flask(__name__, template_folder=template_dir, static_folder='../static')

@app.route('/img/icono_emp.png')
def img():
    return send_from_directory(app.static_folder, 'icono_emp.png')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reg_ventas')
def registros():
    return render_template('registros.html')

@app.route('/b_boleta')
def gboleta():
    return render_template('b_boleta.html')

@app.route('/go_despacho')
def godespacho():
    return render_template('godespacho.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host=None, debug=True)