from flask import Blueprint, request, jsonify
from app.controllers import VehicleController

vehicle_bp = Blueprint('vehicle', __name__)


@vehicle_bp.route('/', methods=['GET'])
def get_vehicles():
    vehicles = VehicleController.get_all_vehicles()
    return jsonify([vehicle.to_dict() for vehicle in vehicles])


@vehicle_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = VehicleController.get_vehicle_by_id(vehicle_id)
    return jsonify(vehicle.to_dict()) if vehicle else ('', 404)


@vehicle_bp.route('/', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    if not data or 'name' not in data or 'salon_id' not in data:
        return ('', 400)
    vehicle = VehicleController.create_vehicle(data)
    return jsonify(vehicle.to_dict()), 201


@vehicle_bp.route('/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    data = request.get_json()
    vehicle = VehicleController.update_vehicle(vehicle_id, data)
    return jsonify(vehicle.to_dict()) if vehicle else ('', 404)


@vehicle_bp.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    success = VehicleController.delete_vehicle(vehicle_id)
    return ('', 204) if success else ('', 404)


@vehicle_bp.route('/<int:vehicle_id>/pay', methods=['POST'])
def pay_monthly_fee(vehicle_id):
    data = request.get_json()
    amount = data.get('amount')
    if amount:
        vehicle = VehicleController.pay_monthly_fee(vehicle_id, amount)
        return jsonify(vehicle.to_dict()) if vehicle else ('', 404)
    return ('Bad Request', 400)
