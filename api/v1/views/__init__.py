#!/usr/bin/python3
from flask import Blueprint


"""creation of a flask blueprint named app_views"""
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
