#!/usr/bin/python3
from models.state import State
from flask import Flask, jsonify,Blueprint , request, abort, make_response
from api.v1.views import app_views
from models import storage
from sqlalchemy.orm import query


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def gets_all_states():
    """gets info about all states from storage"""
    all_states = storage.all(State) .values()
    dict_states= [state.to_dict() for state in all_states]
    return jsonify(dict_states)

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states(state_id):
    """ Retrieves the list of all State objects: GET /api/v1/states
    Retrieves a State object: GET /api/v1/states/<state_id>
    If the state_id is not linked to any State object, raise a 404 error """

    state = storage.get(State, state_id)
    if not state:
        abort (404)
        #return error_404()
    return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def states_delete(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort (404)
        #return error_404()
    storage.delete(State)    
    storage.save()
    storage.close()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post():
    """creating a state using the post request"""
    """this checks if we have json data in request body"""
    if not request.get_json():
        return (jsonify({'error: Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return(jsonify({'error: Missing name'}), 400)
    """creation of new state, we added a state in the request body"""
    state = State(**request.get_json())
    state.save()
    return (jsonify(state.to_dict()), 201)

