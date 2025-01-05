from api.views import app_views
from api.views.auth import isAuthenticated
from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import storage
from models.book import Book

@app_views.route('/books', methods=['GET', 'POST'])
@jwt_required()
def handle_books():
    current_user = isAuthenticated()
    if request.method == 'GET':  # Get all books
        books = storage.all_list(Book)
        if not books:
            return jsonify([])
        return jsonify([book.to_dict() for book in books])
    
    if request.method == 'POST':  # Create a new book
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in data:
            return jsonify({"error": "Missing title"}), 400
        if 'author' not in data:
            return jsonify({"error": "Missing author"}), 400
        if 'genre' not in data:
            return jsonify({"error": "Missing genre"}), 400
        if 'year' not in data:
            return jsonify({"error": "Missing published"}), 400
        data['user_id'] = current_user
        exising_book = storage.get_specific(Book, 'name', data['name'])
        if exising_book:
            return jsonify({"error": "Book already exists"}), 400
        new_book = Book(**data)
        new_book.save()
        return jsonify(new_book.to_dict()), 201
    
@app_views.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_book(book_id):
    current_user = isAuthenticated()
    book = storage.get_specific(Book, 'id', book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    if request.method == 'GET':
        return jsonify(book.to_dict())
    
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['name', 'author', 'genre', 'year']:
                return jsonify({"error": "Invalid attribute"}), 400
            setattr(book, key, value)
        book.save()
        return jsonify(book.to_dict())
    
    if request.method == 'DELETE':
        storage.delete(book)
        storage.save()
        return jsonify({})