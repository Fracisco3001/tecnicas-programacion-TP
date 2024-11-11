from app.app_models.models import Apuesta
from ..extensions import db

class ApuestaDAO:
    @staticmethod
    def obtener_apuestas_por_usuario_id(dniUsuario):
        return Apuesta.query.filter_by(dniUsuario=dniUsuario).all()
    
    @staticmethod
    def crear_apuesta(usuario, carrera, caballo, monto):
        print(usuario)
        print(carrera)
        print(caballo)
        print(monto)
        nueva_apuesta = Apuesta(
            dniUsuario=usuario.dni,
            idCarrera=carrera.idCarrera,
            idCaballo=caballo.idCaballo,
            montoSuspension=monto
        )
        nueva_apuesta.montoVictoria = caballo.calcularPremio(monto)
        db.session.add(nueva_apuesta)
        db.session.commit()
        return 
        
    @staticmethod
    def ver_apuestas_por_carrera(carrera):
        return Apuesta.query.filter_by(idCarrera=carrera.idCarrera).all()
    
    @staticmethod
    def ver_apuestas():
        return Apuesta.query.all()
    
    @staticmethod
    def actualizar_estado_apuesta(idApuesta, estado):
        apuesta = Apuesta.query.filter_by(idApuesta=idApuesta).first()
        apuesta.estado = estado
        db.session.commit()
        return 