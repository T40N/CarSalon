from app.repositories.address_repository import AddressRepository
from app.models.address import Address


class AddressController:

    @staticmethod
    def get_all_addresses():
        return AddressRepository.get_all()

    @staticmethod
    def get_address_by_id(address_id):
        return AddressRepository.get_by_id(address_id)

    @staticmethod
    def create_address(data):
        address = Address(**data)
        return AddressRepository.create(address)

    @staticmethod
    def update_address(address_id, data):
        return AddressRepository.update(address_id, data)

    @staticmethod
    def delete_address(address_id):
        address = AddressRepository.get_by_id(address_id)
        if address:
            AddressRepository.delete(address)
            return True
        return False
