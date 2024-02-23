#!/usr/bin/python3
""" an endpoint that retrieves the number of each objects by type """
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


@app_views.route("/status", methods=['GET'])
def hbnb_stats():
    """returns json status of our flask app"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ return the num of each obj"""
    result = {}
    objc_dict = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    for key, val in objc_dict.items():
        result[val] = storage.count(key)
    return jsonify(result)
