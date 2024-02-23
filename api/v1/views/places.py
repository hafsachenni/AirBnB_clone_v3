#!/usr/bin/python3
"""creating a new view for places that handles api actions/methods"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models.user import User
from models.place import Place
from models.city import City
from models import storage

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """retrieves list of all place objects of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place(place_id):
    """gets one place based on its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())
    
