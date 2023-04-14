#!/usr/bin/python3
"""Endpoints for the reviews class."""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from console import classes


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def reviews_in_place(place_id):
    """ Returns all reviews with the given place id """
    place_list = storage.all(classes["Place"])
    if f"Place.{place_id}" not in place_list:
        abort(404)
    else:
        review_list = []
        all_review = [rv.to_dict()
                      for rv in storage.all(classes.get("Review", 0)).values()]
        for review in all_review:
            if review.get("place_id") == place_id:
                review_list.append(review)
        if review_list is not None:
            return jsonify(review_list)
        else:
            return jsonify([])


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def review_get(review_id):
    """ Returns a review by its id """
    all_review = storage.all(classes["Review"])
    if f"Review.{review_id}" in all_review:
        return jsonify(all_review[f"Review.{review_id}"].to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def review_delete(review_id):
    """ Deletes a Review object from the storage. """
    obj_to_delete = storage.get(classes["Review"], review_id)
    if obj_to_delete:
        storage.delete(obj_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """ Creates a new review with given place id """
    place_list = storage.all(classes["Place"])
    if f"Place.{place_id}" not in place_list:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user_list = storage.all(classes["User"])
    user_id = req["user_id"]
    if f"User.{user_id}" not in user_list:
        abort(404)
    if "text" not in req:
        abort(400, "Missing text")
    review_instance = classes["Review"](**req)
    review_instance.place_id = place_id
    storage.new(review_instance)
    storage.save()
    return review_instance.to_dict(), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def review_update(review_id):
    """ Updates review with given id """
    review_instance = storage.get(classes["Review"], review_id)
    if review_instance:
        try:
            req = request.get_json()
            for key, value in req.items():
                if key != "id" and key != "created_at" and key != "updated_at":
                    if key != "place_id" and key != "user_id":
                        setattr(review_instance, key, value)
            review_instance.save()
            return jsonify(review_instance.to_dict()), 200
        except:
            abort(400, "Not a JSON")
    else:
        abort(404)
