#!/usr/bin/python3
"""creation of a view of review objs using all the different methods"""
from flask import jsonify, abort, make_response, request
from models.place import Place
from api.v1.views import app_views
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if content.get("user_id") is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, content.get("user_id"))
    if user is None:
        abort(404)
    if content.get("text") is None:
        abort(400, 'Missing text')
    new_review = Review(**content)
    new_review.place_id = place.id
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    content = request.get_json()
    list_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in list_keys:
            setattr(review, key, val)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
