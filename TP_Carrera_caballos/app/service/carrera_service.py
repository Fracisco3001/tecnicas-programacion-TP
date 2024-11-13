from app.dao.carrera_dao import CarreraDAO
from app.service.caballo_service import CaballoService
from app.service.carreraCaballo_service import CarreraCaballoService

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
        return ({'mensaje': 'No se encontraron carreras'}, 404, None)
        
    @staticmethod
    def ver_carreras_apostables():
        carreras = CarreraDAO.obtener_carreras_apostables()
        if carreras:
            lista_carreras = []
            for carrera in carreras:
                carrera_dict = carrera.to_dict()
                caballos_response, status_code, caballos = CarreraCaballoService.obtener_caballos_por_carrera(carrera)
                if caballos:
                    carrera_dict["caballos"] = []
                    for caballo in caballos:
                       
                        multiplicador = caballo.get_multiplicador_str()

                        caballo_dict = {
                            "id": caballo.idCaballo,
                            "nombre": caballo.nombreCaballo,
                            "frecuenciaVictoria": caballo.frecuenciaVictoria,  
                            "multiplicador": multiplicador
                        }
                        carrera_dict["caballos"].append(caballo_dict)
                    lista_carreras.append(carrera_dict)
                else:
                    continue

            return {'mensaje': 'Se encontraron las carreras', 'carreras': lista_carreras}, 200
        
        return {'mensaje': 'No se encontraron carreras', 'carreras': []}, 404




    @staticmethod
    def agregar_caballo_a_carrera(idCarrera, idCaballo):
        response, status_code, carrera = CarreraService.obtener_carrera_por_id(idCarrera)
        if not carrera:
            return response, status_code
        response, status_code, caballo = CaballoService.obtener_caballo_por_id(idCaballo)
        if not caballo:
            return response, status_code
        response, status_code, pertenece = CarreraCaballoService.corroborar_caballo_en_carrera(carrera, caballo)
        if carrera.estadoCarrera != 0:
            return {'mensaje':'no se puede agregar caballos a esta altura de la carrera'}, 400
        if pertenece:
            return response, status_code
        CarreraDAO.agregar_caballo_a_carrera(carrera, caballo)
        return {'mensaje': 'Caballo ' + str(caballo.nombreCaballo) + ' agregado a la carrera ' + str(carrera.nombreCarrera)}, 200


    @staticmethod
    def obtener_carrera_por_id(idCarrera):
        carrera = CarreraDAO.obtener_carrera_por_id(idCarrera)
        return  ({'mensaje': 'Carrera encontrado con exito'}, 200, carrera) if carrera else( {'mensaje':'No se encontro ninguna carrera con ese id!'}, 404, None)

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
        if not carrera :
            return {'mensaje': 'No se encontró ninguna carrera con ese ID!'}, 404 
        
        if carrera.estadoCarrera == 2 or carrera.estadoCarrera == 3: #si ya esta terminada o ya esta suspendida no se puede suspender
            return {'mensaje': 'La carrera no se puede suspender'}, 400  
        CarreraDAO.suspender_carrera(carrera.idCarrera)
        return {'mensaje': 'Carrera finalizada con éxito'}, 200  
    
    @staticmethod
    def obtener_carreras():
        carreras = CarreraDAO.obtener_todas_las_carreras()
        if carreras:
            return {'mensaje':'Se encontraron las siguientes carreras'}, 200, carreras
        return {'mensaje':'No se encontraron carreras'}, 404, carreras