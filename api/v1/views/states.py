#!/usr/bin/python3
from models.state import State
from flask import Flask, jsonify,Blueprint , request, abort
from api.v1.views import app_views
from api.v1.app import error_404
from models import storage


@app_views.route("/states/<state_id>", methods=["GET"])
def states(state_id):
    state = storage.get(State, state_id)
    if not state:
        return error_404()
