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
