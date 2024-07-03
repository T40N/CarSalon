from app import db
from app.models import Vehicle


class VehicleRepository:

    @staticmethod
    def get_all():
        return Vehicle.query.all()

    @staticmethod
    def get_by_id(vehicle_id):
        return Vehicle.query.get(vehicle_id)

    @staticmethod
    def create(vehicle):
        db.session.add(vehicle)
        db.session.commit()
        return vehicle

    @staticmethod
    def update(vehicle_id, vehicle_data):
        db.session.query(Vehicle).filter(Vehicle.id == vehicle_id).update(vehicle_data)
        db.session.commit()
        return VehicleRepository.get_by_id(vehicle_id)

    @staticmethod
    def delete(vehicle):
        db.session.delete(vehicle)
        db.session.commit()
