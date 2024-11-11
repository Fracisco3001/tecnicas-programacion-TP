from flask import Flask
from .extensions import db  # Asegúrate de que tengas configuradas las extensiones aquí
from .app_routes.routes import app as routes_bp  # Importa tus rutas

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config.from_pyfile('config.py')  # Asegúrate de tener un archivo de configuración

    # Inicializa las extensiones
    db.init_app(app)

    # Registra las rutas
    app.register_blueprint(routes_bp)

    return app
