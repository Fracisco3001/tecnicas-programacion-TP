from app.service.usuario_service import UsuarioService
from app.service.caballo_service import CaballoService
from app.service.carrera_service import CarreraService
from app.service.carreraCaballo_service import CarreraCaballoService


from app.dao.apuesta_dao import ApuestaDAO

class ApuestaService:

    @staticmethod
    def crear_apuesta(dni, idCarrera, idCaballo, monto):

        response, status_code, usuario = UsuarioService.obtener_usuario_por_dni(dni)
        if not usuario:
            return response, status_code  # Retorna error si el usuario no se encuentra
        
        response, status_code, carrera = CarreraService.obtener_carrera_por_id(idCarrera)
        if not carrera:
            return response, status_code  # Retorna error si la carrera no se encuentra

        response, status_code, caballo = CaballoService.obtener_caballo_por_id(idCaballo)
        if not caballo:
            return response, status_code  # Retorna error si el caballo no se encuentra
        
        response, status_code, pertenece = CarreraCaballoService.corroborar_caballo_en_carrera(carrera, caballo)
        if not pertenece:
            return response, status_code # Devuelve error si el caballo no pertenece a la carrera

        if carrera.estadoCarrera != 0:
            return {'mensaje': 'La carrera no está pendiente'}, 400  # dEVUELVE error si la carrera no esta en el estado que corresponde 

        if usuario.saldo < monto:
            return {'mensaje': 'Saldo insuficiente'}, 400  # 400 #devuelve error si no hay plata

        ApuestaDAO.crear_apuesta(usuario, carrera, caballo, monto)
        UsuarioService.actualizar_saldo_usuario(usuario.dni, (usuario.saldo - monto))

        return {'mensaje':'apuesta creada con exito'}, 200 


    @staticmethod
    def ver_apuestas():
        apuestas = ApuestaDAO.ver_apuestas()
        if apuestas:            
            return {'mensaje': 'se enocntraron apuestas'}, 200, [apuesta.to_dict() for apuesta in apuestas]  
        return {'mensaje':'no se encontraron apuestas'}, 404, None 
    
    @staticmethod
    def ver_apuestas_por_dni(dni):
        response, status_code, usuario = UsuarioService.obtener_usuario_por_dni(dni) 
        if usuario:
            apuestas = ApuestaDAO.obtener_apuestas_por_usuario_id(usuario.dni)
            if apuestas:
                return {'mensaje': 'se encontraron apuestas'}, 200, [apuesta.to_dict() for apuesta in apuestas]  
            return {'mesaje': 'no se encontraron apuestas'}, 404, None
        return response, status_code, None 
    
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
    

    @staticmethod
    def ver_perfil_completo(dni):
        response_usuario, status_code_usuario, usuario = UsuarioService.obtener_usuario_por_dni(dni)
        response_apuestas, status_code_apuestas, apuestas = ApuestaService.ver_apuestas_por_dni(dni)
        if not usuario:
            return response_usuario, status_code_usuario
        response_completo = {
            "usuario": usuario.to_dict(),
            "apuestas": apuestas if apuestas else response_apuestas
        }
        
        status_code = status_code_usuario if status_code_usuario == 200 else status_code_apuestas

        return response_completo, status_code