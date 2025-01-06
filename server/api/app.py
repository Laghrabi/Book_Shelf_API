#!/usr/bin/env python3
""" Starts the Flask web app """
import os
from api.views import app_views
from api.views.auth import jwt
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from models import storage

load_dotenv()
app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Book Shelf API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

jwt.init_app(app)
CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
HOST = "0.0.0.0"
PORT = 5000


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the storage session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Handles the 404 error """
    return jsonify({"error": "Not found"}), 404


@app.route('/static/swagger.yaml')
def serve_swagger_spec():
    return app.send_static_file('swagger.yaml')


if __name__ == "__main__":
    if os.getenv("BOOK_API_HOST"):
        HOST = os.getenv("BOOK_API_HOST")
    if os.getenv("BOOK_API_PORT"):
        PORT = os.getenv("BOOK_API_PORT")
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
