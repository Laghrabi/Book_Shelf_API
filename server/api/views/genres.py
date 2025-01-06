from api.views import app_views
from api.views.auth import isAuthenticated
from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import storage
from models.book import Book
from models.genre import Genre


@app_views.route('/genres', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def handle_genres():
    current_user = isAuthenticated()
    if request.method == 'GET':
        genres = storage.all_list(Genre)
        if not genres:
            return jsonify([])
        return jsonify([genre.to_dict() for genre in genres])

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400
        existing_genre = storage.get_specific(Genre, 'name', data['name'])
        if existing_genre:
            return jsonify({"error": "Genre already exists"}), 400
        new_genre = Genre(**data)
        new_genre.save()
        return jsonify(new_genre.to_dict()), 201


@app_views.route('/genres/<genre_id>', methods=['DELETE'])
@jwt_required()
def delete_genre(genre_id):
    current_user = isAuthenticated()
    genre = storage.get_specific(Genre, 'id', genre_id)
    if not genre:
        return jsonify({"error": "Not found"}), 404
    genre.delete()
    storage.save()
    return jsonify({}), 200
