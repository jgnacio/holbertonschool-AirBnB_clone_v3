#!/usr/bin/python3
"""Endpoints for the city class."""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from console import classes

@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities_in_state(state_id):
    """ Returns all cities with the given state id """
    state_list = storage.all(classes["State"])
    if f"State.{state_id}" not in state_list:
        abort(404)
    else:
        city_list = []
        all_city = [city.to_dict()
                     for city in storage.all(classes.get("City", 0)).values()]
        for city in all_city:
            if city.get("state_id") == state_id:
                city_list.append(city)
        if city_list is not None:
            return jsonify(city_list)
        else:
            return jsonify([])

@app_views.route("/cities/<city_id>", strict_slashes=False)
def city_get(city_id):
    """ Returns a city by its id """
    all_city = storage.all(classes["City"])
    if f"City.{city_id}" in all_city:
        return jsonify(all_city[f"City.{city_id}"].to_dict())
    else:
        abort(404)

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def city_delete(city_id):
    """ Deletes a City object from the storage. """
    obj_to_delete = storage.get(classes["City"], city_id)
    if obj_to_delete:
        storage.delete(obj_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def city_create(state_id):
    """ Creates a new city with given state id """
    req = request.get_json()
    state_list = storage.all(classes["State"])
    if f"State.{state_id}" not in state_list:
        abort(404)
    if "name" in req:
        city_instance = classes["City"]()
        city_instance.name = req["name"]
        city_instance.state_id = state_id
        storage.new(city_instance)
        storage.save()
        return city_instance.to_dict(), 201
    else:
        abort(400, "Missing name")

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_update(city_id):
    """ Updates city with given id """
    city_instance = storage.get(classes["City"], city_id)
    if city_instance:
        try:
            req = request.get_json()
            for key, value in req.items():
                if key != "id" and key != "created_at" and key != "updated_at":
                    if key != "state_id":
                        setattr(city_instance, key, value)
            city_instance.save()
            return jsonify(city_instance.to_dict()), 200
        except:
            abort(400, "Not a JSON")
    else:
        abort(404)
