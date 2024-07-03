from flask import Blueprint, request, jsonify
from app.controllers import SalonController

salon_bp = Blueprint('salon', __name__)


@salon_bp.route('/', methods=['GET'])
def get_salons():
    salons = SalonController.get_all_salons()
    return jsonify([salon.to_dict() for salon in salons])


@salon_bp.route('/<int:salon_id>', methods=['GET'])
def get_salon(salon_id):
    salon = SalonController.get_salon_by_id(salon_id)
    return jsonify(salon.to_dict()) if salon else ('', 404)


@salon_bp.route('/', methods=['POST'])
def create_salon():
    data = request.get_json()
    if not data or 'name' not in data:
        return ('', 400)
    salon = SalonController.create_salon(data)
    return jsonify(salon.to_dict()), 201


@salon_bp.route('/<int:salon_id>', methods=['PUT'])
def update_salon(salon_id):
    data = request.get_json()
    salon = SalonController.update_salon(salon_id, data)
    return jsonify(salon.to_dict()) if salon else ('', 404)


@salon_bp.route('/<int:salon_id>', methods=['DELETE'])
def delete_salon(salon_id):
    success = SalonController.delete_salon(salon_id)
    return ('', 204) if success else ('', 404)
