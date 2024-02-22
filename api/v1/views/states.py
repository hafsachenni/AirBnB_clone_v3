#!/usr/bin/python3
from models.state import State
from flask import Flask, jsonify,Blueprint , request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def gets_all_states():
    """gets info about all states from storage"""
    all_states = storage.all(State) .values()
    dict_states= [state.to_dict() for state in all_states]
    return jsonify(dict_states)

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort (404)
        #return error_404()
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def state_dele(state_id):
    state = storage.get(state, state_id)
    if not state:
        abort (404)
        #return error_404()

    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)