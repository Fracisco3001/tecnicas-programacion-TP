from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from app.dao.usuario_dao import UsuarioDAO

class UsuarioService:
    @staticmethod
    def registrar_usuario(nombre_usuario, email, contraseña, dni, fecha_nacimiento):
        # Verifica si el usuario ya existe
        if UsuarioDAO.obtener_usuario_por_dni(dni):
            return {'mensaje': 'DNI ya registrado'}, 400
        if UsuarioDAO.obtener_usuario_por_email(email):
            return {'mensaje': 'Email ya registrado'}, 400
        
        UsuarioDAO.crear_usuario(nombre_usuario, email, contraseña, dni, fecha_nacimiento)
        return {'mensaje': 'Usuario creado con exito!'}, 201  
    
    @staticmethod
    def logIn(dni, contraseña):

        usuario = UsuarioDAO.obtener_usuario_por_dni(dni)
        if not usuario:
            return {'mensaje': 'Usuario no encontrado!'}, 404
        if not UsuarioDAO.corroborar_contraseña(usuario, contraseña):
            return {'mensaje': 'La contraseña es incorrecta'}, 401
        accesToken = create_access_token(identity=usuario.dni)
        refreshtoken = create_refresh_token(identity=usuario.dni)
        
        return {'mensaje': 'Inicio de sesión exitoso!', 'token': accesToken, 'refreshtoken': refreshtoken}, 200


    @staticmethod
    def actualizar_saldo_usuario(dni, monto):
        UsuarioDAO.actualizar_saldo(dni, monto)
        return {'mensaje': 'Saldo actualizado con exito!'}, 200

    @staticmethod
    def obtener_usuario_por_dni_y_contraseña(dni, contraseña):
        usuario = UsuarioDAO.obtener_usuario_por_dni_y_contraseña(dni, contraseña)
        return ({'mensaje': 'Sesion iniciada con exito!'}, 201) if usuario else ({'mensaje': 'Credenciales incorrectas!'}, 401)

    @staticmethod
    def obtener_usuario_por_dni(dni):
        usuario = UsuarioDAO.obtener_usuario_por_dni(dni)
        return ({'mensaje': 'Usuario encontrado con exito'}, 200, usuario) if usuario else ({'mensaje': 'Usuario no encontrado!'}, 404, None)
   
    @staticmethod
    def obtener_saldo_por_dni(dni):
        usuario = UsuarioDAO.obtener_usuario_por_dni(dni)
        return ({'saldo': usuario.saldo}, 200) if usuario else ({'mensaje': 'Usuario no encontrado'}, 404)  
    
    @staticmethod
    def obtener_usuarios():
        usuarios = UsuarioDAO.obtener_usuarios()
        if usuarios:
            return {'mensaje':'Se encontraron los siguientes usuarios'}, 200, usuarios
        return {'mensaje':'No se encontraron usuarios'}, 404, usuarios