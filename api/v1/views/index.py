#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify


@app_views.route("/status", strict_slashes=False)
def hbnb_stats():
    """returns json status of our flask app"""
    return jsonify({"status": "OK"})
