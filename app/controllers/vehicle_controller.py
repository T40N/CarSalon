from app.repositories.vehicle_repository import VehicleRepository
from app.models.vehicle import Vehicle
from datetime import date


class VehicleController:

    @staticmethod
    def get_all_vehicles():
        return VehicleRepository.get_all()

    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        return VehicleRepository.get_by_id(vehicle_id)

    @staticmethod
    def create_vehicle(data):
        vehicle = Vehicle(**data)
        return VehicleRepository.create(vehicle)

    @staticmethod
    def update_vehicle(vehicle_id, data):
        return VehicleRepository.update(vehicle_id, data)

    @staticmethod
    def delete_vehicle(vehicle_id):
        vehicle = VehicleRepository.get_by_id(vehicle_id)
        if vehicle:
            VehicleRepository.delete(vehicle)
            return True
        return False

    @staticmethod
    def pay_monthly_fee(vehicle_id, amount):
        vehicle = VehicleRepository.get_by_id(vehicle_id)
        if vehicle:
            vehicle.total_cost += amount
            vehicle.last_payment_date = date.today()
            return VehicleRepository.update(vehicle.id, {
                'total_cost': vehicle.total_cost,
                'last_payment_date': vehicle.last_payment_date
            })
        return None
