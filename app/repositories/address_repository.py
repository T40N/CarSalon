from app import db
from app.models import Address


class AddressRepository:

    @staticmethod
    def get_all():
        return Address.query.all()

    @staticmethod
    def get_by_id(address_id):
        return Address.query.get(address_id)

    @staticmethod
    def create(address):
        db.session.add(address)
        db.session.commit()
        return address

    @staticmethod
    def update(address_id, address_data):
        db.session.query(Address).filter(Address.id == address_id).update(address_data)
        db.session.commit()
        return AddressRepository.get_by_id(address_id)

    @staticmethod
    def delete(address):
        db.session.delete(address)
        db.session.commit()
