#Script para crear tablas
#En nuestro caso, ya fueron creadas desde la instancia conectada a Flask
from app import app, db

with app.app_context():
    db.create_all()
    print("All tables created successfully.")
