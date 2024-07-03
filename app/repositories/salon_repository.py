from app import db
from app.models import Salon


class SalonRepository:

    @staticmethod
    def get_all():
        return Salon.query.all()

    @staticmethod
    def get_by_id(salon_id):
        return Salon.query.get(salon_id)

    @staticmethod
    def create(salon):
        db.session.add(salon)
        db.session.commit()
        return salon

    @staticmethod
    def update(salon_id, salon_data):
        db.session.query(Salon).filter(Salon.id == salon_id).update(salon_data)
        db.session.commit()
        return SalonRepository.get_by_id(salon_id)

    @staticmethod
    def delete(salon):
        db.session.delete(salon)
        db.session.commit()
