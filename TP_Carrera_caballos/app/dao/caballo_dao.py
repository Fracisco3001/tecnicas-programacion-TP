from app.app_models.models import Caballo
from ..extensions import db

class CaballoDAO:
    @staticmethod
    def crear_caballo(nombreCaballo, frecuenciaVicotria):
        nuevo_caballo = Caballo(
            nombreCaballo=nombreCaballo,
            frecuenciaVictoria=frecuenciaVicotria
        )        
        db.session.add(nuevo_caballo)
        db.session.commit()
        return
    
    @staticmethod
    def obtener_todos_los_caballos():
        return Caballo.query.all()

    @staticmethod
    def obtener_caballo_por_id(idCaballo):
        return Caballo.query.filter_by(idCaballo=idCaballo).first()
 