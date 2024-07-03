from app.repositories.check_up_repository import CheckUpRepository
from app.models.check_up import CheckUp


class CheckUpController:

    @staticmethod
    def get_all_checkups():
        return CheckUpRepository.get_all()

    @staticmethod
    def get_checkup_by_id(checkup_id):
        return CheckUpRepository.get_by_id(checkup_id)

    @staticmethod
    def create_checkup(data):
        checkup = CheckUp(**data)
        return CheckUpRepository.create(checkup)

    @staticmethod
    def update_checkup(checkup_id, data):
        return CheckUpRepository.update(checkup_id, data)

    @staticmethod
    def delete_checkup(checkup_id):
        checkup = CheckUpRepository.get_by_id(checkup_id)
        if checkup:
            CheckUpRepository.delete(checkup)
            return True
        return False
