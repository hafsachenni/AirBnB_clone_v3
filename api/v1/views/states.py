#!/usr/bin/python3
""" onether view for State objects"""
from models.state import State
from flask import jsonify, Blueprint, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def gets_all_states():
    """gets info about all states from storage"""
    all_states = storage.all(State) .values()
    dict_states = [state.to_dict() for state in all_states]
    return jsonify(dict_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states(state_id):
    """ Retrieves the list of all State objects: GET /api/v1/states
    Retrieves a State object: GET /api/v1/states/<state_id>
    If the state_id is not linked to any State object, raise a 404 error """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def states_delete(state_id):
    """ delete an object in states  """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    """creating a state using the post request"""
    """this checks if we have json data in request body"""
    ask = request.get_json()
    if ask is None:
        abort(400, 'Not a JSON')
    if ask.get("name") is None:
        abort(400, 'Missing name')
    """creation of new state, we added a state in the request body"""
    state = State(**ask)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updating a state object with id using PUT method """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_data = request.get_json()
    if state_data is None:
        abort(400, 'Not a JSON')
    excluded_keys = ['id', 'created_at', 'updated_at']
    for key, val in state_data.items():
        if key not in excluded_keys:
            setattr(state, key, val)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
