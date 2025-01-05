from api.views import app_views
from api.views.auth import isAuthenticated
from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = isAuthenticated()
    user_profile = storage.get_specific(User, 'id', current_user)
    if not user_profile:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_profile.to_dict())

@app_views.route('/users', methods=['DELETE', 'PUT'])
@jwt_required()
def update_user_profile():
    current_user = isAuthenticated()
    user_profile = storage.get_specific(User, 'id', current_user)
    if not user_profile:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'DELETE':
        storage.delete(user_profile)
        storage.save()
        return jsonify({"message": "User profile deleted"}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        if 'first_name' in data:
            user_profile.first_name = data['first_name']
        if 'last_name' in data:
            user_profile.last_name = data['last_name']
        user_profile.updated_at = datetime.now()
        storage.save()
        return jsonify(user_profile.to_dict()), 200
    return jsonify({"error": "Invalid request method"}), 400