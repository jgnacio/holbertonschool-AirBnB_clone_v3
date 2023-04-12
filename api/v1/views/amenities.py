#!/usr/bin/python3
"""Endpoints for the state class."""
from flask import abort
from flask import jsonify
from flask import request
from api.v1.views import app_views
from models import storage
from console import classes


@app_views.route("/amenities", strict_slashes=False)
def get_all_amenities():
    """Return a list of all amenities."""
    amenities_list = [amenity.to_dict()
                   for amenity in storage.all(classes["Amenity"]).values()]
    if amenities_list is not None:
        return jsonify(amenities_list)
    else:
        return jsonify([])


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Return a amenity by its id."""
    all_amenity = storage.all(classes["Amenity"])
    if f"State.{amenity_id}" in all_amenity:
        return jsonify(all_amenity[f"State.{amenity_id}"].to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a State object from the storage."""
    amenity_instance = storage.get(classes["Amenity"], amenity_id)
    if amenity_instance:
        storage.delete(amenity_instance)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create a new amenity."""
    try:
        req = request.get_json()
        if "name" in req:
            amenity_instance = classes["Amenity"]()
            amenity_instance.name = req["name"]
            storage.new(amenity_instance)
            storage.save()
            return amenity_instance.to_dict(), 201
        else:
            abort(400, "Missing name")
    except:
        abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Update the atributes of a amenity instance."""
    amenity_instance = storage.get(classes["Amenity"], amenity_id)
    if amenity_instance:
        try:
            req = request.get_json()
            for key, value in req.items():
                if key != "id" and key != "created_at" and key != "updated_at":
                    setattr(amenity_instance, key, value)
            amenity_instance.save()
            return jsonify(amenity_instance.to_dict()), 200
        except:
            abort(400, "Not a JSON")
    else:
        abort(404)
