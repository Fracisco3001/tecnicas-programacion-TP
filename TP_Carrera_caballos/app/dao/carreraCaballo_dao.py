from app_models.models import Carrera  # Supón que ya tienes el modelo CarreraCaballo

class CarreraCaballoService:
    @staticmethod
    def obtener_caballos_por_carrera(id_carrera):
        carrera = Carrera.query.get(id_carrera)
        if carrera:
            return carrera.caballos 
        return None