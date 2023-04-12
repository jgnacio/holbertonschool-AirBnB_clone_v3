#!/usr/bin/python3
"""Contains the application configuration."""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(resp):
    """Close the storage instance."""
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    return {"error": "Not found"}, 404

if __name__ == '__main__':
    api_host = getenv("HBNB_API_HOST")
    api_port = getenv("HBNB_API_PORT")
    if api_host is None:
        api_host = "0.0.0.0"
    if api_port is None:
        api_port = "5000"

    app.run(host=api_host, port=api_port, threaded=True, debug=True)
