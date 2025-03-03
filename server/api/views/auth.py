from api.views import app_views
from flask import jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity)
from models import storage
from models.user import User


jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return storage.get(User, identity)


def isAuthenticated():
    """Get the current user"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'error': 'Invalid token'}), 401
    return current_user


@app_views.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email or not password or not first_name or not last_name:
        return jsonify({'error': 'Missing required fields'}), 400

    if storage.get_specific(User, 'email', email):
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(**data)

    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing email or password'}), 400

    email = data['email']
    password = data['password']

    user = storage.get_specific(User, 'email', email)

    if not user or user.verify_password(password, user.password) is False:
        return jsonify({'error': 'Invalid email or password'}), 401

    token = create_access_token(identity=user)
    return jsonify({'token': token})
