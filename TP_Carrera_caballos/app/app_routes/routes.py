from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from app.extensions import db  # Asegúrate de usar la ruta correcta
from datetime import datetime

from app.service.carreraCaballo_service import CarreraCaballoService
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
   

    response, status_code = ApuestaService.ver_perfil_completo(dni)
    
    return response, status_code

@app.route('/ver_apuestas_realizadas', methods=['GET'])
@jwt_required()
def apuestas_realizadas():
    dni = get_jwt_identity()

    response, status_code, apuestas = ApuestaService.ver_apuestas_por_dni(dni)
    
    return (apuestas, status_code) if apuestas else (response, status_code)


@app.route('/realizar_apuesta', methods=['POST'])
@jwt_required()
def realizar_apuesta():
    data = request.get_json()

    dni = get_jwt_identity()
    idCarrera = data.get('idCarrera')
    idCaballo = data.get('idCaballo')
    monto = data.get('monto')

    response, status_code = ApuestaService.crear_apuesta(dni, idCarrera, idCaballo, monto)

    return response, status_code

@app.route('/ver_carreras_apostables', methods=['GET'])
@jwt_required()
def ver_carreas_apostables():

    response, status_code = CarreraService.ver_carreras_apostables()
    
    return jsonify(response), status_code



@app.route('/ver_todos_usuarios', methods=['GET'])
@jwt_required()
def ver_todos_usuarios():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401

    response, status_code, usuarios = UsuarioService.obtener_usuarios()

    if usuarios:
        usuarios_dict = [usuario.to_dict() for usuario in usuarios]
        return jsonify(usuarios_dict), status_code

    return jsonify(response), status_code



@app.route('/ver_datos_usuario', methods=['GET'])
@jwt_required()
def ver_datos_usuario():

    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401    
    
    data = request.get_json()
    
    dni = data.get('dni')
    
    response, status_code, usuario = UsuarioService.obtener_usuario_por_dni(dni)
    
    return (usuario.to_dict(), status_code) if usuario else (response, status_code)



@app.route('/ver_carreras', methods=['GET'])
@jwt_required()
def ver_carreras():
    
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401    
    
    response, status_code, carreras = CarreraService.ver_carreras()
    
    if carreras:
        return jsonify({'mensaje': response['mensaje'], 'carreras': carreras}), status_code
    return jsonify(response), status_code


@app.route('/ver_caballos', methods=['GET'])
@jwt_required()
def ver_caballos():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401        
    response, status_code, caballos = CaballoService.ver_caballos()
    
    if caballos:
        return jsonify({'mensaje': response['mensaje'], 'caballos': caballos}), status_code
    return jsonify(response), status_code



@app.route('/ver_apuestas', methods=['GET'])
@jwt_required()
def ver_apuestas():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401    
    response, status_code, apuestas = ApuestaService.ver_apuestas()
    if apuestas:
        return apuestas
    return jsonify(response), status_code




@app.route('/iniciar_carrera', methods=['PUT'])
@jwt_required()
def iniciar_carrera():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401        
    data = request.get_json()
    
    idCarrera = data.get('idCarrera')

    response, status_code = CasinoService.iniciar_carrera(idCarrera)
    return response, status_code


@app.route('/finalizar_carrera', methods=['PUT'])
@jwt_required()
def finalizar_carrera():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401    
    data = request.get_json()
    
    idCarrera = data.get('idCarrera')

    response, status_code = CasinoService.finalizar_carrera(idCarrera)
    return response, status_code




@app.route('/suspender_carrera', methods=['PUT'])
@jwt_required()
def suspender_carrera():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401    
    data = request.get_json()
    
    idCarrera = data.get('idCarrera')

    response, status_code = CasinoService.suspender_carrera(idCarrera)
    return response, status_code


@app.route('/crear_caballo', methods=['POST'])
@jwt_required()
def crear_caballo():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401    
    data = request.json

    nombreCaballo = data.get('nombreCaballo')
    frecuenciaVictoria = data.get('frecuenciaVictoria')

    response, status_code = CaballoService.crear_caballo(nombreCaballo, frecuenciaVictoria)  

    return response, status_code

@app.route('/crear_carrera', methods=['POST'])
@jwt_required()
def crear_carrera():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401    
    data = request.json

    nombreCarrera = data.get('nombreCarrera')

    response, status_code = CarreraService.crear_carrera(nombreCarrera)  

    return response, status_code


@app.route('/agregar_caballo_a_carrera', methods=['POST'])
@jwt_required()
def relacionar_caballo():
    rol = get_jwt()['role']
    if not corroborarAdmin(rol):
        return {'mensaje':'el usuario no es administrador'}, 401        
    data = request.json

    idCaballo = data.get('idCaballo')
    idCarrera = data.get('idCarrera')

    response, status_code = CarreraService.agregar_caballo_a_carrera(idCarrera, idCaballo)

    return response, status_code

def corroborarAdmin(string):
    return string == 'admin'



#ATAJAR ERRORES BDD (TRY AND CATCH)


