import os
from flask import Flask
import configparser
from .extensions import db, jwt
from app.app_routes.routes import app as routes_bp

config = configparser.ConfigParser()
config.read('main.conf')
key = config.get('JWT', 'SECRET_KEY')
port = key = config.get('MAINWORK', 'PORT')

def create_app(config=None):

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = key  # Debe ser segura y almacenada de forma segura
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900  # 15 minutos


    if config:
        app.config.update(config)
    else:
        database_path = os.path.join(app.instance_path, 'database.db')
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=port)
