#!/usr/bin/python3
"""Metrics Routes"""
from api.views import app_views


@app_views.route('/status')
def status():
    """Return the API status all wrapped in a json object"""
    return {"status": "OK"}, 200


@app_views.route('stats')
def stats():
    """Return the count of all classes"""
    from models.book import Book
    from models.genre import Genre
    from models.user import User
    from models.user_book import UserBook
    from models import storage

    return {
            "Users": storage.count(User),
            "Books": storage.count(Book),
            "Genres": storage.count(Genre),
            "User_books": storage.count(UserBook)
            }