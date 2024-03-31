#!/usr/bin/python3
""" other view for User objects that handles all default RESTFul API actions """
from models.user import User
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects """
    users = storage.all(User).values()
    dict_users = [user.to_dict() for user in users]
    return jsonify(dict_users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a User """
    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, 'Not a JSON')
    email = user_data.get("email")
    if email is None:
        abort(400, 'Missing email')
    password = user_data.get("password")
    if password is None:
        abort(400, 'Missing password')
    user = User(**user_data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, 'Not a JSON')
    excluded_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, val in user_data.items():
        if key not in excluded_keys:
            setattr(user, key, val)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
