from app.repositories import VehicleRepository
from app.repositories import UserRepository
from app.models import User


class UserController:

    @staticmethod
    def get_all_users():
        return UserRepository.get_all()

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def create_user(data):
        user = User(**data)
        return UserRepository.create(user)

    @staticmethod
    def update_user(user_id, data):
        return UserRepository.update(user_id, data)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if user:
            UserRepository.delete(user)
            return True
        return False

    @staticmethod
    def assign_vehicle_to_user(user_id, vehicle_id):
        user = UserRepository.get_by_id(user_id)
        vehicle = VehicleRepository.get_by_id(vehicle_id)
        if user and vehicle:
            vehicle.user_id = user.id
            VehicleRepository.update(vehicle.id, {'user_id': user.id})
            return user
        return None
