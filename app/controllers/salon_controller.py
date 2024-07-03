from app.models import Salon
from app.repositories.salon_repository import SalonRepository


class SalonController:

    @staticmethod
    def get_all_salons():
        return SalonRepository.get_all()

    @staticmethod
    def get_salon_by_id(salon_id):
        return SalonRepository.get_by_id(salon_id)

    @staticmethod
    def create_salon(data):
        salon = Salon(**data)
        return SalonRepository.create(salon)

    @staticmethod
    def update_salon(salon_id, data):
        return SalonRepository.update(salon_id, data)

    @staticmethod
    def delete_salon(salon_id):
        salon = SalonRepository.get_by_id(salon_id)
        if salon:
            SalonRepository.delete(salon)
            return True
        return False
