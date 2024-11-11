from app.app_models.models import Carrera
from ..extensions import db

class CarreraDAO:

    @staticmethod
    def agregar_caballo_a_carrera(carrera, caballo):
        carrera.caballos.append(caballo)
        db.session.commit()
        return


    @staticmethod
    def crear_carrera(nombreCarrera):
        nueva_carrera = Carrera(
            nombreCarrera=nombreCarrera
        )        
        db.session.add(nueva_carrera)
        db.session.commit()
        return
        
    @staticmethod
    def iniciar_carrera(idCarrera):
        carrera = Carrera.query.filter_by(idCarrera=idCarrera).first() 
        carrera.iniciar()
        db.session.commit()
        return 
    
    @staticmethod
    def finalizar_carrera(idCarrera):
        carrera = Carrera.query.filter_by(idCarrera=idCarrera).first() 
        carrera.finalizar()
        db.session.commit()
        return 
    
    @staticmethod
    def suspender_carrera(idCarrera):
        carrera = Carrera.query.filter_by(idCarrera=idCarrera).first() 
        carrera.suspender()
        db.session.commit()
        return 

    @staticmethod
    def obtener_todas_las_carreras():
        return Carrera.query.all()
    
    @staticmethod
    def obtener_carrera_por_id(idCarrera):
        return Carrera.query.filter_by(idCarrera=idCarrera).first()
