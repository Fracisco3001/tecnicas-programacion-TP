import pytest
from app.main import create_app
from app.extensions import db
from app.models import Usuario, Carrera, Caballo, Apuesta, Casino


@pytest.fixture()
def client():
    # Crear la app con configuración de base de datos en memoria
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Base de datos en memoria para pruebas
    })

    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos de prueba

    # Iniciar el cliente de pruebas
    with app.test_client() as client:
        yield client  # Se pasa el cliente al test

    # Limpiar la base de datos después de cada test
    with app.app_context():
        db.drop_all()

def test_app_initialization():
    app = create_app()
    with app.app_context():
        assert db is not None
        assert db.engine is not None

def test_registrar_usuario(client):
    response = client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['mensaje'] == 'Usuario registrado exitosamente'

    # Verificar que el usuario se ha guardado en la base de datos
    usuario = Usuario.query.filter_by(dni='12345678').first()
    assert usuario is not None
    assert usuario.nombreUsuario == 'test_user'



def test_registrar_usuario_con_dni_duplicado(client):
    # Registrar el primer usuario
    response = client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })
    assert response.status_code == 201  # Asegúrate de que se registró correctamente
    response = client.post('/registrar', json={
        'dni': '12345678',  # Usando el mismo DNI
        'nombreUsuario': 'another_user',
        'email': 'another_user@example.com',
        'contraseña': 'password456',
        'fechaNacimiento': '1990-01-01'
    })
    
    
    assert response.status_code == 409  # Debe fallar debido a DNI duplicado
    data = response.get_json()
    assert data['mensaje'] == 'DNI ya registrado'


def test_iniciar_sesion_exitoso(client):
    # Registrar primero un usuario
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })

    # Probar el inicio de sesión con las credenciales correctas
    response = client.post('/iniciar_sesion', json={
        'dni': '12345678',
        'contraseña': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['mensaje'] == 'Inicio de sesión exitoso'

def test_iniciar_sesion_fallido(client):
    # Probar el inicio de sesión con credenciales incorrectas
    response = client.post('/iniciar_sesion', json={
        'dni': '12345678',
        'contraseña': 'wrongpassword'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data['mensaje'] == 'Credenciales incorrectas'
    

def test_ver_saldo(client):
    # Registrar primero un usuario
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })

    # Verificar el saldo inicial (asumiendo que es 0 por defecto)
    response = client.get('/ver_saldo/12345678')
    assert response.status_code == 200
    data = response.get_json()
    assert data['saldo'] == 100.00



def test_iniciar_carrera(client):
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })
    carrera = Carrera(nombreCarrera="Carrera 1")
    db.session.add(carrera)
    db.session.commit()
    response = client.post(f'/iniciar_carrera/{carrera.idCarrera}')
    
    # Verifica que la respuesta tenga un código de estado 200
    assert response.status_code == 200
    carrera = db.session.get(Carrera, carrera.idCarrera)
    assert carrera.estadoCarrera == 1


def test_finalizar_carrera(client):
    # Registrar un usuario
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })

    # Crear carrera
    carrera = Carrera(nombreCarrera="Carrera de Prueba", estadoCarrera=1)  # Estado 1: en proceso
    db.session.add(carrera)
    db.session.commit()

    # Crear caballos con valores correctos
    caballo1 = Caballo(nombreCaballo="carlos", frecuenciaVictoria=2)
    caballo2 = Caballo(nombreCaballo="juan", frecuenciaVictoria=7)

    # Agregar caballos a la sesión
    db.session.add(caballo1)
    db.session.add(caballo2)
    db.session.commit()  # Confirma los cambios

    # Obtener los IDs de los caballos después del commit
    caballo1 = db.session.query(Caballo).filter_by(nombreCaballo="carlos").first()
    caballo2 = db.session.query(Caballo).filter_by(nombreCaballo="juan").first()

    client.post(f'/relacionar_caballo/{carrera.idCarrera}', json={
        'idCaballo': caballo1.idCaballo  # Usar el ID del caballo 1
    })

    client.post(f'/relacionar_caballo/{carrera.idCarrera}', json={
        'idCaballo': caballo2.idCaballo,  # Usar el ID del caballo 2
    })

    response = client.post(f'/finalizar_carrera/{carrera.idCarrera}')
    assert response.status_code == 200

    # Verificar que el estado de la carrera se actualizó
    carrera = db.session.get(Carrera, carrera.idCarrera)
    assert carrera.estadoCarrera == 2  # Estado 2: finalizada






#APUESTAS
def test_realizar_apuesta_en_carrera_no_pendiente(client):
    # Registrar usuario con saldo inicial
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })

    # Crear carrera y caballo
    carrera = Carrera(nombreCarrera="Carrera 1", estadoCarrera=1)  # Estado "en proceso"
    db.session.add(carrera)
    db.session.commit()

    caballo = Caballo(nombreCaballo="Caballo 1", frecuenciaVictoria=5)
    db.session.add(caballo)
    db.session.commit()
    
    # Intentar realizar una apuesta
    response = client.post('/realizar_apuesta', json={
        'dni': '12345678',
        'monto': 100.0,
        'idCarrera': carrera.idCarrera,
        'idCaballo': caballo.idCaballo
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data['mensaje'] == 'La carrera no está pendiente'


def test_realizar_apuesta_con_caballo_no_en_carrera(client):
    # Registrar usuario con saldo inicial
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })

    # Crear carrera
    carrera = Carrera(nombreCarrera="Carrera 1")
    db.session.add(carrera)
    db.session.commit()

    # Crear caballo que no se añadirá a la carrera
    caballo_no_en_carrera = Caballo(nombreCaballo="Caballo 1", frecuenciaVictoria=5)
    db.session.add(caballo_no_en_carrera)
    db.session.commit()

    # Crear otro caballo que sí estará en la carrera
    caballo_en_carrera = Caballo(nombreCaballo="Caballo 2", frecuenciaVictoria=3)
    db.session.add(caballo_en_carrera)
    db.session.commit()

    # Relacionar el caballo correcto con la carrera
    carrera.caballos.append(caballo_en_carrera)
    db.session.commit()

    # Intentar realizar una apuesta con el caballo que no está en la carrera
    response = client.post('/realizar_apuesta', json={
        'dni': '12345678',
        'monto': 100.0,
        'idCarrera': carrera.idCarrera,
        'idCaballo': caballo_no_en_carrera.idCaballo
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data['mensaje'] == 'El caballo no está en la carrera'



def test_ver_apuestas(client):
    # Registrar usuario y realizar una apuesta
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })

    # Probar la consulta de apuestas con el DNI del usuario
    response = client.get('/ver_apuestas/12345678')  # Se usa el DNI en lugar del ID de usuario
    assert response.status_code == 200  # Asegúrate de que no es 404
    data = response.get_json()
    assert 'apuestas' in data



def test_realizar_apuesta_con_saldo_insuficiente(client):
    # Registrar usuario
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user',
        'email': 'test_user@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })
    usuario = Usuario.query.filter_by(dni='12345678').first()
    usuario.saldo = 10.0
    db.session.commit()

    carrera = Carrera(nombreCarrera="Carrera 1")
    db.session.add(carrera)
    db.session.commit()

    caballo = Caballo(nombreCaballo="Caballo 1", frecuenciaVictoria=5)

    db.session.add(caballo)
    db.session.commit()

    # Intentar realizar una apuesta mayor que el saldo
    response = client.post('/realizar_apuesta', json={
        'dni': '12345678',
        'monto': 20.0,  # Monto mayor que el saldo
        'idCarrera': carrera.idCarrera,
        'idCaballo': caballo.idCaballo
    })
    assert response.status_code == 400  # Debe fallar debido a saldo insuficiente
    data = response.get_json()
    assert data['mensaje'] == 'Saldo insuficiente'


def test_realizar_apuesta_y_pago_en_casino(client):
    casino = Casino()
    # Registrar primer usuario con saldo
    client.post('/registrar', json={
        'dni': '12345678',
        'nombreUsuario': 'test_user_1',
        'email': 'test_user_1@example.com',
        'contraseña': 'password123',
        'fechaNacimiento': '1990-01-01'
    })
    usuario1 = Usuario.query.filter_by(dni='12345678').first()
    usuario1.saldo = 100.0  # Asignar saldo inicial
    db.session.add(usuario1)
    db.session.commit()

    # Registrar segundo usuario con saldo
    client.post('/registrar', json={
        'dni': '87654321',
        'nombreUsuario': 'test_user_2',
        'email': 'test_user_2@example.com',
        'contraseña': 'password456',
        'fechaNacimiento': '1992-01-01'
    })
    usuario2 = Usuario.query.filter_by(dni='87654321').first()
    usuario2.saldo = 100.0  # Asignar saldo inicial
    db.session.add(usuario2)
    db.session.commit()

    # Crear carrera
    carrera = casino.crear_carrera(nombreCarrera="Carrera 1")
    
    # Crear caballos
    caballo1 = Caballo(nombreCaballo="Caballo 1", frecuenciaVictoria=10)
    caballo2 = Caballo(nombreCaballo="Caballo 2", frecuenciaVictoria=5)
    db.session.add(caballo1)
    db.session.add(caballo2)
    db.session.commit()

    # Relacionar caballos con la carrera
    carrera.caballos.append(caballo1)
    carrera.caballos.append(caballo2)
    db.session.commit()
    usuario1 = Usuario.query.filter_by(dni='12345678').first()
    usuario2 = Usuario.query.filter_by(dni='87654321').first()
    caballo1 = Caballo.query.filter_by(nombreCaballo="Caballo 1").first()
    caballo2 = Caballo.query.filter_by(nombreCaballo="Caballo 2").first()
    # Realizar apuestas
    apuesta1 = casino.crear_apuesta(usuario1.dni, 50.0, carrera.idCarrera, caballo1.idCaballo)
    apuesta2 = casino.crear_apuesta(usuario2.dni, 50.0, carrera.idCarrera, caballo2.idCaballo)

    assert apuesta1 is not None
    assert apuesta2 is not None

    # Simular el resultado de la carrera y finalizarla
    carrera.ganador_id = caballo1.idCaballo  # Supongamos que el caballo 1 gana
    carrera.estadoCarrera = 2  # Cambiar estado a finalizada
    db.session.commit()

    # Distribuir premios a los ganadores
    casino.distribuir_premios(carrera)

    # Verificar el saldo de los usuarios después del pago
    usuario1_actualizado = Usuario.query.filter_by(dni='12345678').first()
    usuario2_actualizado = Usuario.query.filter_by(dni='87654321').first()

    assert usuario1_actualizado.saldo == 105  # 100.0 + premio
    assert usuario2_actualizado.saldo == 50   # 100.0 - 30.0 (no ganó)

def test_singleton_casino(client):
    # Verificar que la clase Casino actúa como Singleton
    casino1 = Casino()
    casino2 = Casino()

    assert casino1 is casino2  # Verificar que ambas referencias son al mismo objeto

def test_crear_carrera_en_casino(client):
    # Obtener la instancia de Casino (Singleton)
    casino = Casino()
    client.post('/registrar', json={
        'dni': '87654321',
        'nombreUsuario': 'test_user_2',
        'email': 'test_user_2@example.com',
        'contraseña': 'password456',
        'fechaNacimiento': '1992-01-01'
    })
    # Crear una nueva carrera en el casino
    carrera = casino.crear_carrera("Gran Premio")

    # Verificar que la carrera ha sido creada correctamente
    assert carrera is not None
    assert carrera.nombreCarrera == "Gran Premio"
    assert carrera.estadoCarrera == 0  # La carrera debería estar en estado pendiente

    # Verificar que la carrera está registrada en el sistema
    carrera_en_db = Carrera.query.filter_by(nombreCarrera="Gran Premio").first()
    assert carrera_en_db is not None



def test_agregar_usuario_en_casino(client):
    # Obtener la instancia de Casino (Singleton)
    casino = Casino()
    dni = 87654321
    client.post('/registrar', json={
        'dni': '87654321',
        'nombreUsuario': 'user_test',
        'email': 'test_user_2@example.com',
        'contraseña': 'password456',
        'fechaNacimiento': '1992-01-01'
    })
    # Crear un nuevo usuario
    casino.crear_usuario("12345678", "user_test2", "test2@example.com", "password", "1990-01-01")        
    usuario = Usuario.query.filter_by(dni="12345678").first()
    # Verificar que el usuario ha sido creado correctamente
    assert usuario is not None
    assert usuario.dni == "12345678"
    assert usuario.nombreUsuario == "user_test2"
    
    # Verificar que el usuario está registrado en la base de datos
    usuario_en_db = Usuario.query.filter_by(dni="12345678").first()
    assert usuario_en_db is not None