class CarreraCaballoService:
    @staticmethod
    def obtener_caballos_por_carrera(carrera):
        if not carrera.caballos:
            return {'mensaje':'No hay caballos para esta carrera'}, 404, None
        return {'mensaje':'Encontrados los caballos para la carrera'}, 200, carrera.caballos
    
    @staticmethod
    def corroborar_caballo_en_carrera(carrera, caballo):
        response, status_code, caballos = CarreraCaballoService.obtener_caballos_por_carrera(carrera)
        if not caballos:
             return response, status_code, False
        
        for caballoLista in caballos:
            if int(caballoLista.idCaballo)==int(caballo.idCaballo):
                return {'mensaje':'El caballo ya pertenece a la carrera'}, 400, True
        return {'mensaje':'El caballo no pertenece a la carrera'}, 400, False
    
