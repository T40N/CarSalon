from flask import Blueprint, request, jsonify
from app.controllers import CheckUpController

checkup_bp = Blueprint('checkup', __name__)


@checkup_bp.route('/', methods=['GET'])
def get_checkups():
    checkups = CheckUpController.get_all_checkups()
    return jsonify([checkup.to_dict() for checkup in checkups])


@checkup_bp.route('/<int:checkup_id>', methods=['GET'])
def get_checkup(checkup_id):
    checkup = CheckUpController.get_checkup_by_id(checkup_id)
    return jsonify(checkup.to_dict()) if checkup else ('', 404)


@checkup_bp.route('/', methods=['POST'])
def create_checkup():
    data = request.get_json()
    if not data or 'last_checkup_date' not in data or 'vehicle_id' not in data:
        return ('', 400)
    checkup = CheckUpController.create_checkup(data)
    return jsonify(checkup.to_dict()), 201


@checkup_bp.route('/<int:checkup_id>', methods=['PUT'])
def update_checkup(checkup_id):
    data = request.get_json()
    checkup = CheckUpController.update_checkup(checkup_id, data)
    return jsonify(checkup.to_dict()) if checkup else ('', 404)


@checkup_bp.route('/<int:checkup_id>', methods=['DELETE'])
def delete_checkup(checkup_id):
    success = CheckUpController.delete_checkup(checkup_id)
    return ('', 204) if success else ('', 404)
