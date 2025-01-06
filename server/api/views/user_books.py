from api.views import app_views
from api.views.auth import isAuthenticated
from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import storage
from models.book import Book
from models.user_book import UserBook


@app_views.route('/user_books', methods=['GET', 'POST'])
@jwt_required()
def handle_user_books():
    current_user = isAuthenticated()
    if request.method == 'GET':
        user_books = storage.all_list(UserBook)
        if not user_books:
            return jsonify([])
        return jsonify([user_book.to_dict() for user_book in user_books])

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'book_id' not in data:
            return jsonify({"error": "Missing book_id"}), 400
        book = storage.get_specific(Book, 'id', data['book_id'])
        if not book:
            return jsonify({"error": "Book not found"}), 404
        if storage.get_specific(UserBook, 'book_id', book.id):
            return jsonify({
                "error": "User Book relationship already exists"
                }), 409
        new_user_book = UserBook(user_id=current_user, book_id=book.id)
        if 'read' in data and type(data['read']) is bool:
            new_user_book.read = data['read']
        if 'like' in data and type(data['like']) is bool:
            new_user_book.like = data['like']
        new_user_book.save()
        return jsonify(new_user_book.to_dict()), 201


@app_views.route('/user_books/<user_book_id>',
                 methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_user_book(user_book_id):
    current_user = isAuthenticated()
    user_book = storage.get_specific(UserBook, 'id', user_book_id)
    if not user_book:
        return jsonify({"error": "No User Book relationship found"}), 404
    if user_book.user_id != current_user:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        return jsonify(user_book.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'read' in data and type(data['read']) is bool:
            user_book.read = data['read']
        if 'like' in data and type(data['like']) is bool:
            user_book.like = data['like']
        user_book.updated_at = datetime.now()
        user_book.save()
        return jsonify(user_book.to_dict())

    if request.method == 'DELETE':
        user_book.delete()
        return jsonify({})


@app_views.route('/user_books/likes', methods=['GET'])
@jwt_required()
def get_user_likes():
    current_user = isAuthenticated()
    user_books = storage.all_list_specific(UserBook, 'user_id', current_user)
    if not user_books:
        return jsonify([])
    likes = [user_book.to_dict() for user_book in user_books if user_book.like]
    return jsonify(likes)


@app_views.route('/user_books/reads', methods=['GET'])
@jwt_required()
def get_user_reads():
    current_user = isAuthenticated()
    user_books = storage.all_list_specific(UserBook, 'user_id', current_user)
    if not user_books:
        return jsonify([])
    reads = [user_book.to_dict() for user_book in user_books if user_book.read]
    return jsonify(reads)
