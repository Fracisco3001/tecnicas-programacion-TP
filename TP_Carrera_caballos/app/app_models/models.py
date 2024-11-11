from sqlalchemy import CheckConstraint
from werkzeug.security import generate_password_hash ,check_password_hash
from ..extensions import db 
import random

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    fechaNacimiento = db.Column(db.DateTime, nullable=False)
    saldo = db.Column(db.Float, default=100)

    def __init__(self, nombreUsuario, email, contraseña, dni, fechaNacimiento):
        self.nombreUsuario = nombreUsuario
        self.email = email
        self.contraseña = self.crear_contraseña(contraseña)
        self.dni = dni
        self.fechaNacimiento = fechaNacimiento

    def crear_contraseña(self, contraseña):
        return generate_password_hash(contraseña)
    
    def corroborar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña) 

    def to_dict(self):
        resultado = {
            'Nombre': self.nombreUsuario,
            'dni': self.dni,
            'email': self.email, 
            'saldo': self.saldo 
        }
        
        return resultado

class Carrera(db.Model):
    __tablename__ = 'carreras' 
    idCarrera = db.Column(db.Integer, primary_key=True)
    nombreCarrera = db.Column(db.String(100), nullable=False)
    ganador_id = db.Column(db.Integer, db.ForeignKey('caballos.idCaballo'))
    estadoCarrera = db.Column(db.Integer, default=0)  # 0: Pendiente, 1: En Proceso, 2: Finalizada, 3: Suspendida
    caballos = db.relationship('Caballo', secondary='carreras_caballo', backref='carreras')

    def iniciar(self):
        self.estadoCarrera = 1

    def finalizar(self):
        self.estadoCarrera = 2
        ganador = self.determinar_ganador()
        if ganador:
            self.ganador_id = ganador.idCaballo  # Establecer el ganador
        return "La carrera no está en estado 'En Proceso'"

    def determinar_ganador(self): #algoritmo con el que defino que caballo gana, usa la frecuencia de victoria de cada caballo para darle mas o menos oportunidades de ganar
        caballos_validos = [caballo for caballo in self.caballos] 
        if caballos_validos:  # Solo proceder si hay caballos válidos
            weights = [caballo.frecuenciaVictoria for caballo in caballos_validos] 
            return random.choices(caballos_validos, weights=weights, k=1)[0]  # Retornar el caballo ganador
        else:
            return None 
        
    def suspender(self):
        self.estadoCarrera = 3


    def to_dict(self):
        estado_texto = {
            0: "Pendiente",
            1: "En Proceso",
            2: "Finalizada",
            3: "Suspendida"
        }.get(self.estadoCarrera, "Desconocido") 

        resultado = {
            'idCarrera': self.idCarrera,
            'nombreCarrera': self.nombreCarrera,
            'estadoCarrera': estado_texto
        }

        if hasattr(self, 'ganador_id') and self.ganador_id is not None:
            resultado['ganador_id'] = self.ganador_id

        return resultado

    
class Caballo(db.Model):
    __tablename__ = 'caballos'
    idCaballo = db.Column(db.Integer, primary_key=True)
    nombreCaballo = db.Column(db.String(100), nullable=False)
    frecuenciaVictoria = db.Column(db.Integer, CheckConstraint('frecuenciaVictoria > 0'), nullable=False)
    
    def calcularPremio(self, montoApostado):
        premio_adicional = montoApostado * (1 / self.frecuenciaVictoria)
        premio_total = montoApostado + premio_adicional
        return premio_total
    

    carrera_caballo = db.Table('carreras_caballo',
        db.Column('idCarrera', db.Integer, db.ForeignKey('carreras.idCarrera'), primary_key=True),
        db.Column('idCaballo', db.Integer, db.ForeignKey('caballos.idCaballo'), primary_key=True)
    )

    def to_dict(self):
        return {
            "id_caballo": self.idCaballo,
            "nombre_caballo": self.nombreCaballo,
            "frecuencia_victoria": self.frecuenciaVictoria
        } 

class Apuesta(db.Model):
    __tablename__ = 'apuestas'
    idApuesta = db.Column(db.Integer, primary_key=True)
    dniUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    idCarrera = db.Column(db.Integer, db.ForeignKey('carreras.idCarrera'), nullable=False)  
    idCaballo = db.Column(db.Integer, db.ForeignKey('caballos.idCaballo'), nullable=False)  # Relación con el caballo apostado
    montoVictoria = db.Column(db.Float)
    montoSuspension = db.Column(db.Float)
    estado = db.Column(db.Integer, default=0) #0 para no pagada, 1 para pagada

    usuario = db.relationship('Usuario', backref='apuestas')  # Relación en SQLAlchemy
    carrera = db.relationship('Carrera', backref='apuestas')
    caballo = db.relationship('Caballo', backref='apuestas')

    def to_dict(self):
        estado_str = "No pagada" if self.estado == 0 else "Pagada"
        return {
            "id_apuesta": self.idApuesta,
            "dni_usuario": self.dniUsuario,
            "id_carrera": self.idCarrera,
            "id_caballo": self.idCaballo,
            "monto_victoria": self.montoVictoria,
            "monto_suspension": self.montoSuspension,
            "estado": estado_str
        }


class Casino:  
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Casino, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if not self.initialized:  # Evitar re-inicialización
            self.carreras = []
            self.apuestas = []
            self.usuarios = []
            self.initialized = True
    
    @classmethod
    def getInstance(cls):
        return cls._instance

    def to_dict(self):
        return {
            "carreras": [carrera for carrera in self.carreras],
            "apuestas": [apuesta for apuesta in self.apuestas],
            "usuarios": [usuario for usuario in self.usuarios]
        }
