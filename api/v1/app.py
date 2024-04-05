#!/usr/bin/python3
""" this is an app instance of Flask """

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["0.0.0.0"])

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """ closes connection/sql session on teardown """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ return a dic error """
    error_dic = {"error": "Not found"}
    return jsonify(error_dic), 404


if __name__ == "__main__":
    """this is our main flask applicataion"""
    """and we are retrieving the value of environment vars"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
