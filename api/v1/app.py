#!/usr/bin/python3
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close(exception):
    """ closes connection/sql session on teardown """
    storage.close()

@app.errorhandler(404)
def error_404(arror):
    error_dic = {"error": "Not found"}
    return jsonify(error_dic)

if __name__ == "__main__":
    """this is our main flask applicataion"""
    """and we are retrieving the value of environment vars"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
