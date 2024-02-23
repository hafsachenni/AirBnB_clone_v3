#!/usr/bin/python3
"""creation of a new view for User that handles default api actions"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """retrieving a list of all users from storage"""
    users = storage.all(User).values()
    user = [user.to_dict() for user in users]
    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """retriveving a user from storage based on its provided user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deleting a user based on id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """posting a new user"""
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json(silent=True):
        abort(400, 'Missing email')
    if 'password' not in request.get_json(silent=True):
        abort(400, 'Missing password')
    new_user = User(**request.get_json(silent=True))
    storage.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """putting/updating a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    """iterating through each key/value in the request body"""
    for key, value in request.get_json().items(silent=True):
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            """setting value of attr"""
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict(), 200)
