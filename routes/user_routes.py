from flask import Blueprint, request, jsonify
import json
from services import user_service

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def home():
    return "User Management System"

@user_routes.route('/users', methods=['GET'])
def get_all_users():
    users = user_service.get_all_users()
    return jsonify(users)

@user_routes.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        return jsonify(user)
    else:
        return "User not found", 404

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_service.create_user(data['name'], data['email'], data['password'])
    return "User created", 201

@user_routes.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if 'name' in data and 'email' in data:
        user_service.update_user(user_id, data['name'], data['email'])
        return "User updated"
    return "Invalid data", 400

@user_routes.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_service.delete_user(user_id)
    return f"User {user_id} deleted"

@user_routes.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return "Please provide a name to search", 400
    users = user_service.search_users_by_name(name)
    return jsonify(users)

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_service.login_user(data['email'], data['password'])
    if user:
        return jsonify({"status": "success", "user_id": user[0]})
    else:
        return jsonify({"status": "failed"})
