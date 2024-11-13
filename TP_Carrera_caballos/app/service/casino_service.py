from app.app_models.models import Casino
from app.service.apuesta_service import ApuestaService
from app.service.carrera_service import CarreraService
from app.service.usuario_service import UsuarioService

class CasinoService:
    
    @staticmethod
    def cargar_datos(casino):
        casino.carreras = CarreraService.obtener_carreras()[2]
        casino.apuestas = ApuestaService.obtener_apuestas()[2]
        casino.usuarios = UsuarioService.obtener_usuarios()[2]
        return casino
    
    @staticmethod
    def obtener_casino():
        casino = Casino()
        casino = CasinoService.cargar_datos(casino)
        return casino
    
class CasinoService:

    @staticmethod
    def iniciar_carrera(id_carrera):

        response, status_code = CarreraService.iniciar_carrera(id_carrera)
        return response, status_code



    @staticmethod
    def finalizar_carrera(id_carrera):

        response, status_code = CarreraService.finalizar_carrera(id_carrera)
        if status_code != 200:
            return response, status_code

        return CasinoService.distribuir_premios(id_carrera, es_suspension=False)

    @staticmethod
    def suspender_carrera(id_carrera):

        response, status_code = CarreraService.suspender_carrera(id_carrera)
        if status_code != 200:
            return response, status_code

        return CasinoService.distribuir_premios(id_carrera, es_suspension=True)

    @staticmethod
    def distribuir_premios(id_carrera, es_suspension):

        response, status_code, carrera = CarreraService.obtener_carrera_por_id(id_carrera)
        if status_code != 200 or not carrera:
            return response, 404
        response, status_code, apuestas = ApuestaService.ver_apuestas_por_carrera(carrera)
        if not apuestas:
            return {"mensaje": "Carrera finalizada sin apuestas"}, 200

        resultado = {"apuestas_actualizadas": 0, "usuarios_actualizados": []}
        for apuesta in apuestas:
            if apuesta.estado == 0: # Solo procesar apuestas en estado "Esperando" (estado == 0)
                if es_suspension:    # Si es suspensión, actualizar el estado a "Suspensión" y otorgar monto de suspensión
                    monto_premio = apuesta.montoSuspension
                    response, status_code, usuario = UsuarioService.obtener_usuario_por_dni(apuesta.dniUsuario)
                    if usuario:
                        nuevo_saldo = usuario.saldo + monto_premio
                        response, status_code = UsuarioService.actualizar_saldo_usuario(apuesta.dniUsuario, nuevo_saldo)
                        if status_code == 200:
                            ApuestaService.actualizar_estado_apuesta(apuesta.idApuesta, 3)  # Estado a "Suspensión"
                            resultado["apuestas_actualizadas"] += 1
                            resultado["usuarios_actualizados"].append(apuesta.dniUsuario)
                else:
                    # Si no es suspensión, procesar como ganadora o perdedora
                    if apuesta.idCaballo == carrera.ganador_id:
                        monto_premio = apuesta.montoVictoria
                        response, status_code, usuario = UsuarioService.obtener_usuario_por_dni(apuesta.dniUsuario)
                        if usuario:
                            nuevo_saldo = usuario.saldo + monto_premio
                            response, status_code = UsuarioService.actualizar_saldo_usuario(apuesta.dniUsuario, nuevo_saldo)
                            if status_code == 200:
                                ApuestaService.actualizar_estado_apuesta(apuesta.idApuesta, 1)  # Estado a "Victoria"
                                resultado["apuestas_actualizadas"] += 1
                                resultado["usuarios_actualizados"].append(apuesta.dniUsuario)
                    else:
                        ApuestaService.actualizar_estado_apuesta(apuesta.idApuesta, 2)  # Estado a "Derrota"
                        resultado["apuestas_actualizadas"] += 1

        return resultado, 200


    

    def actualizar_saldo_si_apuesta_ganada(dni_usuario, monto):
        UsuarioService.actualizar_saldo_usuario(dni_usuario, monto)

