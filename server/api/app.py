#!/usr/bin/env python3
""" Starts the Flask web app """
import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage


load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
app.url_map.strict_slashes = False
HOST = "0.0.0.0"
PORT = 5000


# To be removed att deployement
@app.route('/volumes')
def volume():
    """ A dummy route to test volumes of docker"""
    return "Testing volumes: -<Chaimae>-"


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the storage session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Handles the 404 error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if os.getenv("BOOK_API_HOST"):
        HOST = os.getenv("BOOK_API_HOST")
    if os.getenv("BOOK_API_PORT"):
        PORT = os.getenv("BOOK_API_PORT")
    app.run(host=HOST, port=PORT, threaded=True, debug=True)