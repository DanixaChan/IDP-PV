# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user1:user123@172.31.27.200:3306/idp-pv-1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # URL del endpoint de AWS EC2 para obtener los datos de despacho
    API_DESPACHOS_URL = 'http://44.205.221.190:8000/despachos/'
    # URL de la API externa para obtener los datos de las boletas
    API_BOLETAS_URL = 'https://api_externa_boletas.com/boletas'
