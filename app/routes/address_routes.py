from flask import Blueprint, request, jsonify
from app.controllers import AddressController

address_bp = Blueprint('address', __name__)


@address_bp.route('/', methods=['GET'])
def get_addresses():
    addresses = AddressController.get_all_addresses()
    return jsonify([address.to_dict() for address in addresses])


@address_bp.route('/<int:address_id>', methods=['GET'])
def get_address(address_id):
    address = AddressController.get_address_by_id(address_id)
    return jsonify(address.to_dict()) if address else ('', 404)


@address_bp.route('/', methods=['POST'])
def create_address():
    data = request.get_json()
    if not data or 'street' not in data or 'city' not in data or 'state' not in data or 'zip_code' not in data or 'salon_id' not in data:
        return ('', 400)
    address = AddressController.create_address(data)
    return jsonify(address.to_dict()), 201


@address_bp.route('/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    data = request.get_json()
    address = AddressController.update_address(address_id, data)
    return jsonify(address.to_dict()) if address else ('', 404)


@address_bp.route('/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    success = AddressController.delete_address(address_id)
    return ('', 204) if success else ('', 404)
