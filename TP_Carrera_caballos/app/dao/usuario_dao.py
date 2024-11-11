from app.app_models.models import Usuario
from ..extensions import db

class UsuarioDAO:
    @staticmethod
    def crear_usuario(nombre_usuario, email, contraseña, dni, fecha_nacimiento):
        usuario = Usuario(
            nombreUsuario=nombre_usuario,
            email=email,
            contraseña=contraseña,
            dni=dni,
            fechaNacimiento=fecha_nacimiento
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def actualizar_saldo(dni, nuevo_saldo):
        usuario = UsuarioDAO.obtener_usuario_por_dni(dni)
        usuario.saldo = nuevo_saldo
        db.session.commit()
        return usuario

    def corroborar_contraseña(usuario, contraseña):
        return usuario.corroborar_contraseña(contraseña)
    
    @staticmethod
    def obtener_usuarios():
        return Usuario.query.all()

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def obtener_usuario_por_dni(dni):
        return Usuario.query.filter_by(dni=dni).first()
    
    @staticmethod
    def obtener_usuario_por_email(email):
        return Usuario.query.filter_by(email=email).first()
    
    @staticmethod #log in 
    def obtener_usuario_por_dni_y_contraseña(dni, contraseña):
        return Usuario.query.filter_by(dni=dni, contraseña=contraseña).first()
    



