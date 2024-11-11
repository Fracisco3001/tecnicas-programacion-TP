from app.service.usuario_service import UsuarioService
from app.service.caballo_service import CaballoService
from app.service.carrera_service import CarreraService

from app.dao.apuesta_dao import ApuestaDAO

class ApuestaService:

    @staticmethod
    def crear_apuesta(dni, idCarrera, idCaballo, monto):
        usuario_response, usuario_status, usuario = UsuarioService.obtener_usuario_por_dni(dni)
        if usuario_status != 200:
            return usuario_response, usuario_status  # Retorna error si el usuario no se encuentra
        
        carrera_response, carrera_status, carrera = CarreraService.obtener_carrera_por_id(idCarrera)
        if carrera_status != 200:
            return carrera_response, carrera_status  # Retorna error si la carrera no se encuentra

        caballo_response, caballo_status, caballo = CaballoService.obtener_caballo_por_id(idCaballo)
        if caballo_status != 200:
            return caballo_response, caballo_status  # Retorna error si el caballo no se encuentra

        if carrera.estadoCarrera != 0:
            return {'mensaje': 'La carrera no está pendiente'}, 400  # 400 Bad Request

        if usuario.saldo < monto:
            return {'mensaje': 'Saldo insuficiente'}, 400  # 400 Bad Request

        ApuestaDAO.crear_apuesta(usuario, carrera, caballo, monto)
        UsuarioService.actualizar_saldo_usuario(usuario.idUsuario, (usuario.saldo - monto))
        return {'mensaje':'apuesta creada con exito'}, 200 


    @staticmethod
    def ver_apuestas(dni):
        response, status_code, usuario = UsuarioService.obtener_usuario_por_dni(dni) 
        if usuario:
            apuestas = ApuestaDAO.obtener_apuestas_por_usuario_id(usuario.dni)
            return {'apuestas': [apuesta.to_dict() for apuesta in apuestas]}, status_code  # 200 OK
        return response, status_code  # 404 Not Found
    
    @staticmethod
    def ver_apuestas_por_carrera(carrera):
        apuestas = ApuestaDAO.ver_apuestas_por_carrera(carrera)
        if apuestas:
            return {'mensaje': 'Se encontraron las siguentes apuesta para esta carrera'}, 200, apuestas  
        return {'mensaje': 'no se encontraron apuestas para esta carrera'}, 404, apuestas  
                
                
    @staticmethod
    def obtener_apuestas():
        apuestas = ApuestaDAO.ver_apuestas()
        if apuestas:
            return {'mensaje':'Se encontraron las siguientes apuestas'}, 200, apuestas
        return {'mensaje':'No se encontraron apuestas'}, 404, apuestas
    
                
    @staticmethod
    def actualizar_estado_apuesta(idApuesta, estado):
        ApuestaDAO.actualizar_estado_apuesta(idApuesta, estado)
        return {'mensaje':'apuesta actualizada con exito'}, 200 
    