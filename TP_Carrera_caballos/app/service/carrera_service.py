from app.dao.carrera_dao import CarreraDAO
from app.service.caballo_service import CaballoService

class CarreraService:
        
    @staticmethod
    def crear_carrera(nombreCarrera):
        CarreraDAO.crear_carrera(nombreCarrera)
        return {'mensaje': 'Carrera creada con exito'}, 200

    @staticmethod
    def ver_carreras():
        carreras = CarreraDAO.obtener_todas_las_carreras()
        if carreras:
            lista_carreras = [carrera.to_dict() for carrera in carreras]
            return ({'mensaje': 'Se encontraron las carreras'}, 200, lista_carreras)
        return ({'mensaje': 'No se encontraron carreras'}, 404, carreras)
        
    @staticmethod
    def agregar_caballo_a_carrera(idCarrera, idCaballo):
        carrera = CarreraDAO.obtener_carrera_por_id(idCarrera)
        response, status_code, caballo = CaballoService.obtener_caballo_por_id(idCaballo)
        if(status_code!=200):
            return response, status_code
        
        CarreraDAO.agregar_caballo_a_carrera(carrera, caballo)
        return {'mensaje': 'Caballo ' + str(caballo.nombreCaballo) + ' agregado a la carrera ' + str(carrera.nombreCarrera)}, 200


    @staticmethod
    def obtener_carrera_por_id(idCarrera):
        carrera = CarreraDAO.obtener_carrera_por_id(idCarrera)
        return  ({'mensaje': 'Carrera encontrado con exito'}, 200, carrera) if carrera else( {'mensaje':'No se encontro ningun caballo con ese id!'}, 404)

    @staticmethod
    def iniciar_carrera(idCarrera):
        carrera = CarreraDAO.obtener_carrera_por_id(idCarrera)
        if carrera is None:
            return {'mensaje': 'No se encontró ninguna carrera con ese ID!'}, 404  # 404 Not Found

        if carrera.estadoCarrera != 0:
            return {'mensaje': 'La carrera no está en estado pendiente (0)'}, 400  # 400 Bad Request
        
        if not carrera.caballos:
            return {'mensaje': 'La carrera no tiene caballos'}, 400  # 400 Bad Request
        
        CarreraDAO.iniciar_carrera(carrera.idCarrera)  
        return {'mensaje': 'Carrera iniciada con éxito'}, 200  # 200 OK

    @staticmethod
    def finalizar_carrera(idCarrera):
        carrera = CarreraDAO.obtener_carrera_por_id(idCarrera)
        if carrera is None:
            return {'mensaje': 'No se encontró ninguna carrera con ese ID!'}, 404  # 404 Not Found

        if carrera.estadoCarrera != 1:
            return {'mensaje': 'La carrera no está en estado "En Proceso" (1)'}, 400  # 400 Bad Request
       
        CarreraDAO.finalizar_carrera(carrera.idCarrera)
        return {'mensaje': 'Carrera finalizada con éxito'}, 200  
    

    @staticmethod
    def suspender_carrera(idCarrera):
        carrera = CarreraDAO.obtener_carrera_por_id(idCarrera)
        if carrera is None:
            return {'mensaje': 'No se encontró ninguna carrera con ese ID!'}, 404  # 404 Not Found

        CarreraDAO.suspender_carrera(carrera.idCarrera)
        return {'mensaje': 'Carrera finalizada con éxito'}, 200  
    
    @staticmethod
    def obtener_carreras():
        carreras = CarreraDAO.obtener_todas_las_carreras()
        if carreras:
            return {'mensaje':'Se encontraron las siguientes carreras'}, 200, carreras
        return {'mensaje':'No se encontraron carreras'}, 404, carreras