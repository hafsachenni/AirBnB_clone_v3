#!/usr/bin/python3
""" an endpoint that retrieves the number of each objects by type """
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


@app_views.route("/status", methods=['GET'])
def hbnb_stats():
    """returns json status of our flask app"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type  """
    stats_dic = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(stats_dic)
