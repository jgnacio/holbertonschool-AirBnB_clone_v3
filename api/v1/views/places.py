#!/usr/bin/python3
"""Endpoints for the city class."""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from console import classes


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def places_in_city(city_id):
    """ Returns all places with the given city id """
    city_list = storage.all(classes["City"])
    if f"City.{city_id}" not in city_list:
        abort(404)
    else:
        places_list = []
        all_places = [plac.to_dict()
                      for plac in storage.all(classes.get("Place", 0)).values()]
        for place in all_places:
            if place.get("city_id") == city_id:
                places_list.append(place)
        if places_list is not None:
            return jsonify(places_list)
        else:
            return jsonify([])


@app_views.route("/places/<place_id>", strict_slashes=False)
def place_get(place_id):
    """ Returns a place by its id """
    all_places = storage.all(classes["Place"])
    if f"Place.{place_id}" in all_places:
        return jsonify(all_places[f"Place.{place_id}"].to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def place_delete(place_id):
    """ Deletes a Place object from the storage. """
    obj_to_delete = storage.get(classes["Place"], place_id)
    if obj_to_delete:
        storage.delete(obj_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """ Creates a new place with given city id """
    city_list = storage.all(classes["City"])
    if f"City.{city_id}" not in city_list:
        abort(404)
    try:
        req = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user_list = storage.all(classes["User"])
    user_id = req["user_id"]
    if f"User.{user_id}" not in user_list:
        abort(404)
    if "name" in req:
        place_instance = classes["Place"]()
        place_instance.name = req["name"]
        place_instance.city_id = city_id
        place_instance.user_id = user_id
        storage.new(place_instance)
        storage.save()
        return place_instance.to_dict(), 201
    else:
        abort(400, "Missing name")


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_update(place_id):
    """ Updates place with given id """
    place_instance = storage.get(classes["Place"], place_id)
    if place_instance:
        try:
            req = request.get_json()
            for key, value in req.items():
                if key != "id" and key != "created_at" and key != "updated_at":
                    if key != "city_id":
                        setattr(place_instance, key, value)
            place_instance.save()
            return jsonify(place_instance.to_dict()), 200
        except:
            abort(400, "Not a JSON")
    else:
        abort(404)
