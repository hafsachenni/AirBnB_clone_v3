#!/usr/bin/python3
"""creating a new view for places that handles api actions/methods"""

from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models.user import User
from models.place import Place
from models.city import City
from models import storage


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
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


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place based on its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """posting a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    ask = request.get_json(silent=True)
    if ask is None:
        abort(400, 'Not a JSON')
    if ask.get("user_id") is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, ask['user_id'])
    if user is None:
        abort(404)
    if ask.get("name") is None:
        abort(400, 'Missing name')
    ask['city_id'] = city_id
    place2 = Place(**ask)
    storage.save()
    return make_response(jsonify(place2.to_dict()), 201)


@app_views.route(
        '/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """putting a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    key_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request.get_json(silent=True).items():
        if key not in key_list:
            setattr(place, key, value)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)
