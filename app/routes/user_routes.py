from flask import Blueprint, request, jsonify
from app.controllers import UserController

user_bp = Blueprint('user', __name__)


@user_bp.route('/', methods=['GET'])
def get_users():
    users = UserController.get_all_users()
    return jsonify([user.to_dict() for user in users])


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserController.get_user_by_id(user_id)
    return jsonify(user.to_dict()) if user else ('', 404)


@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return ('', 400)
    user = UserController.create_user(data)
    return jsonify(user.to_dict()), 201


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = UserController.update_user(user_id, data)
    return jsonify(user.to_dict()) if user else ('', 404)


@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserController.delete_user(user_id)
    return ('', 204) if success else ('', 404)
