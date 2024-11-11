from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
import jwt
from app.extensions import db  # Asegúrate de usar la ruta correcta
from datetime import datetime

from app.service.casino_service import CasinoService
from app.service.apuesta_service import ApuestaService
from app.service.usuario_service import UsuarioService  
from app.service.carrera_service import CarreraService  
from app.service.caballo_service import CaballoService 

app = Blueprint('routes', __name__)



@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    data = request.json
    
    nombre_usuario = data.get('nombreUsuario')
    email = data.get('email')
    contraseña = data.get('contraseña')
    dni = data.get('dni')
    fecha_nacimiento = datetime.strptime(data['fechaNacimiento'], '%Y-%m-%d')

    response, status_code = UsuarioService.registrar_usuario(
        nombre_usuario, email, contraseña, dni, fecha_nacimiento
    )

    return jsonify (response), status_code 


@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    data = request.json

    dni = data.get('dni')
    contraseña = data.get('contraseña')

    response, status_code = UsuarioService.logIn(
        dni, contraseña
    )

    return jsonify (response), status_code 

@app.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    dni = get_jwt_identity()

    response, status_code, usuario = UsuarioService.obtener_usuario_por_dni(dni)
    
    return (usuario.to_dict(), status_code) if usuario else (response, status_code)

@app.route('/ver_carreras', methods=['GET'])
def ver_carreras():
    
    response, status_code, carreras = CarreraService.ver_carreras()
    
    if carreras:
        return jsonify({'mensaje': response['mensaje'], 'carreras': carreras}), status_code
    return jsonify(response), status_code


@app.route('/ver_caballos', methods=['GET'])
def ver_caballos():
    
    response, status_code, caballos = CaballoService.ver_caballos()
    
    if caballos:
        return jsonify({'mensaje': response['mensaje'], 'caballos': caballos}), status_code
    return jsonify(response), status_code

@app.route('/ver_datos_usuario', methods=['GET'])
def ver_datos_usuario():
    data = request.get_json()
    
    dni = data.get('dni')
    
    response, status_code, usuario = UsuarioService.obtener_usuario_por_dni(dni)
    
    return (usuario.to_dict(), status_code) if usuario else (response, status_code)


@app.route('/ver_saldo', methods=['GET'])
def ver_saldo():
    data = request.get_json()
    
    dni = data.get('dni')

    response, status_code = UsuarioService.obtener_saldo_por_dni(dni)
    return jsonify(response), status_code


@app.route('/ver_apuestas', methods=['GET'])
def ver_apuestas():
    data = request.get_json()

    dni = data.get('dni')

    response, status_code = ApuestaService.ver_apuestas(dni)
    return jsonify(response), status_code


@app.route('/realizar_apuesta', methods=['POST'])
def realizar_apuesta():
    data = request.get_json()
    
    dni = data.get('dni')
    idCarrera = data.get('idCarrera')
    idCaballo = data.get('idCaballo')
    monto = data.get('monto')

    response, status_code = ApuestaService.crear_apuesta(dni, idCarrera, idCaballo, monto)


    return response, status_code


@app.route('/iniciar_carrera', methods=['POST'])
def iniciar_carrera():
    data = request.get_json()
    
    idCarrera = data.get('idCarrera')

    response, status_code = CarreraService.iniciar_carrera(idCarrera)
    return response, status_code


@app.route('/finalizar_carrera', methods=['POST'])
def finalizar_carrera():
    data = request.get_json()
    
    idCarrera = data.get('idCarrera')

    response, status_code = CasinoService.finalizar_carrera(idCarrera, False)
    return response, status_code


@app.route('/crear_caballo', methods=['POST'])
def crear_caballo():
    data = request.json

    nombreCaballo = data.get('nombreCaballo')
    frecuenciaVictoria = data.get('frecuenciaVictoria')

    response, status_code = CaballoService.crear_caballo(nombreCaballo, frecuenciaVictoria)  

    return response, status_code

@app.route('/crear_carrera', methods=['POST'])
def crear_carrera():
    data = request.json

    nombreCarrera = data.get('nombreCarrera')

    response, status_code = CarreraService.crear_carrera(nombreCarrera)  

    return response, status_code


@app.route('/agregar_caballo_a_carrera', methods=['POST'])
def relacionar_caballo():
    data = request.json

    idCaballo = data.get('idCaballo')
    idCarrera = data.get('idCarrera')

    response, status_code = CarreraService.agregar_caballo_a_carrera(idCarrera, idCaballo)

    return response, status_code


#agregar json web tokens                                        LISTO
#agregar cuenta de admin para operar sobre todo                 
#usar casino?
#hacer el pago de las apuestas y similares (contemplar suspension)
#que no se pueda apostar a un caballo que no esta en una carrera