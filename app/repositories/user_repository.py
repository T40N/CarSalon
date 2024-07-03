from app import db
from app.models import User


class UserRepository:

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create(user):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user_id, user_data):
        db.session.query(User).filter(User.id == user_id).update(user_data)
        db.session.commit()
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()
