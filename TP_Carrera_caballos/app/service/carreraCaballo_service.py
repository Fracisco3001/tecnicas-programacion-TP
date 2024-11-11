from app.dao.carreraCaballo_dao import CarreraCaballoDAO  # Supón que ya tienes un DAO para esta tabla

class CarreraCaballoService:
    @staticmethod
    def obtener_carrera_caballo(id_carrera):
        return CarreraCaballoDAO.obtener_por_id_carrera(id_carrera)