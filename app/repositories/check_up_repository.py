from app import db
from app.models import CheckUp


class CheckUpRepository:

    @staticmethod
    def get_all():
        return CheckUp.query.all()

    @staticmethod
    def get_by_id(checkup_id):
        return CheckUp.query.get(checkup_id)

    @staticmethod
    def create(checkup):
        db.session.add(checkup)
        db.session.commit()
        return checkup

    @staticmethod
    def update(checkup_id, checkup_data):
        db.session.query(CheckUp).filter(CheckUp.id == checkup_id).update(checkup_data)
        db.session.commit()
        return CheckUpRepository.get_by_id(checkup_id)

    @staticmethod
    def delete(checkup):
        db.session.delete(checkup)
        db.session.commit()
