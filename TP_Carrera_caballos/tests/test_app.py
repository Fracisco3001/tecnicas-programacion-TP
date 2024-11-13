from flask_jwt_extended import create_access_token
import pytest
from app.main import create_app
from app.extensions import db

@pytest.fixture()
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  #Base de datos en memoria para pruebas
    })

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        with app.app_context():  
            yield client  

def test_app_initialization():
    app = create_app()
    with app.app_context():
        assert db is not None
        assert db.engine is not None


#Helpers
def get_admin_token():
    return create_access_token(identity="admin_dni", additional_claims={"role": "admin"})

def get_user_token():
    return create_access_token(identity="user_dni", additional_claims={"role": "user"})

#TESTS

def test_registrar_usuario(client):
    response = client.post('/registrar_usuario', json={
        'nombreUsuario': 'testuser',
        'email': 'testuser@example.com',
        'contraseña': 'password123',
        'dni': '12345678',
        'fechaNacimiento': '1990-01-01'
    })
    assert response.status_code == 201

def test_registrar_usuario_duplicado(client):
    response = client.post('/registrar_usuario', json={
        'nombreUsuario': 'testuser',
        'email': 'testuser@example.com',
        'contraseña': 'password123',
        'dni': '12345678',
        'fechaNacimiento': '1990-01-01'
    })
    response = client.post('/registrar_usuario', json={
        'nombreUsuario': 'testuser',
        'email': 'testuser@example.com',
        'contraseña': 'password123',
        'dni': '12345678',
        'fechaNacimiento': '1990-01-01'
    })
    assert response.status_code == 400

def test_iniciar_sesion(client):
    client.post('/registrar_usuario', json={
        'nombreUsuario': 'testuser',
        'email': 'testuser@example.com',
        'contraseña': 'password123',
        'dni': '12345678',
        'fechaNacimiento': '1990-01-01'
    })
    response = client.post('/iniciar_sesion', json={
        'dni': '12345678',
        'contraseña': 'password123'
    })
    assert response.status_code == 200

def test_iniciar_sesion_incorrecto(client):
    client.post('/registrar_usuario', json={
        'nombreUsuario': 'testuser',
        'email': 'testuser@example.com',
        'contraseña': 'password123',
        'dni': '12345678',
        'fechaNacimiento': '1990-01-01'
    })
    response = client.post('/iniciar_sesion', json={
        'dni': '12345678',
        'contraseña': 'wrong123'
    })
    assert response.status_code == 401


def test_perfil(client):
    access_token = get_user_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    client.post('/registrar_usuario', json={
        'nombreUsuario': 'Test User',
        'email': 'testuser@example.com',
        'contraseña': 'securepassword',
        'dni': 'user_dni',
        'fechaNacimiento': '1990-01-01'
    })
    response = client.get('/perfil', headers=headers)
    assert response.status_code == 200

def test_ver_todos_usuarios(client):
    access_token = get_admin_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    
    client.post('/registrar_usuario', json={
        'nombreUsuario': 'Test User',
        'email': 'testuser@example.com',
        'contraseña': 'securepassword',
        'dni': 'user_dni',
        'fechaNacimiento': '1990-01-01'
    })

    response = client.get('/ver_todos_usuarios', headers=headers)
    assert response.status_code == 200


def test_crear_carrera(client):
    access_token = get_admin_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/crear_carrera', headers=headers, json={
        'nombreCarrera': 'Gran Premio'
    })
    assert response.status_code == 200

def test_realizar_apuesta(client):
    access_token_user = get_user_token()
    headers_user = {'Authorization': f'Bearer {access_token_user}'}

    access_token_admin = get_admin_token()
    headers_admin = {'Authorization': f'Bearer {access_token_admin}'}

    client.post('/registrar_usuario', json={
        'nombreUsuario': 'Test User',
        'email': 'testuser@example.com',
        'contraseña': 'securepassword',
        'dni': 'user_dni',
        'fechaNacimiento': '1990-01-01'
    })

    client.post('/crear_carrera', headers=headers_admin, json={
        'nombreCarrera': 'Gran Premio'
    })

    client.post('/crear_caballo', headers=headers_admin, json={
        'nombreCaballo': 'Caballo Rápido',
        'frecuenciaVictoria': 70
    })
    
    client.post('/agregar_caballo_a_carrera', headers=headers_admin, json={
        'idCarrera': 1,
        'idCaballo': 1
    })

    response = client.post('/realizar_apuesta', headers=headers_user, json={
        'dni': 'user_dni',
        'idCarrera': 1,
        'idCaballo': 1,
        'monto': 100
    })
    assert response.status_code == 200
