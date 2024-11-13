from app.app_models.models import Caballo
from app.dao.caballo_dao import CaballoDAO

class CaballoService:

    @staticmethod
    def crear_caballo(nombreCaballo, frecuenciaVicotria):
        CaballoDAO.crear_caballo(nombreCaballo, frecuenciaVicotria)
        return {'mensaje': 'Caballo creado con exito'}, 200


    @staticmethod
    def obtener_caballo_por_id(idCaballo):
        caballo = CaballoDAO.obtener_caballo_por_id(idCaballo=idCaballo)
        return  ({'mensaje': 'Caballo encontrado con exito'}, 200, caballo) if caballo else ({'mensaje':'No se encontro ningun caballo con ese id!'}, 404, None)
    

    @staticmethod
    def ver_caballos():
        caballos = CaballoDAO.obtener_todos_los_caballos()
        if caballos:
            lista_caballos = [caballo.to_dict() for caballo in caballos]
            return ({'mensaje': 'Se encontraron los caballos'}, 200, lista_caballos)
        return ({'mensaje': 'No se encontraron caballos'}, 404, None)
       