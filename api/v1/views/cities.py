#!/usr/bin/python3
"""Cities handler"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, request, jsonify

@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities_in_state(state_id):
    """ Returns all cities with the given state id """
    key_list = []
    for key in storage.all(State).keys():
        key_list.append(key.split('.')[1])
    if state_id not in key_list:
        abort(404)
    cities_list = []
    for value in storage.all(City).values():
        if state_id == value.to_dict().get('state_id'):
            cities_list.append(value.to_dict())
    return jsonify(cities_list)

@app_views.route("/cities/<city_id>", strict_slashes=False)
def city_get(city_id):
    """ Returns city """
    key_list = []
    for key in storage.all(City).keys():
        key_list.append(key.split('.')[1])
    if city_id not in key_list:
        abort(404)
    else:
        return jsonify(storage.get(City, city_id).to_dict())

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def city_delete(city_id):
    """ Deletes city based on id """
    key_list = []
    for key in storage.all(City).keys():
        key_list.append(key.split('.')[1])
    if city_id not in key_list:
        abort(404)
    else:
        storage.delete(storage.get(City, city_id))
        storage.save()
        return jsonify({}), 200

@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def city_create(state_id):
    """ Creates a new city with given state id """
    try:
        city_request = request.get_json()
        city_id = city_request.get('city_id')
        key_list = []
        for key in storage.all(State).keys():
            key_list.append(key.split('.')[1])
        if state_id not in key_list:
            abort(404)
        if "name" not in city_request:
            abort(400, "Missing name")
        key_list.clear()
        new_city = City()
        new_city.name = city_request.get("name")
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    except:
        abort(400, "Not a JSON")

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_update(city_id):
    """ Updates city with given id """
    try:
        city_request = request.get_json()
        key_list = []
        for key in storage.all(City).keys():
            key_list.append(key.split('.')[1])
        if city_id not in key_list:
            abort(404)
        city_upd = storage.all(City).get(City, city_id)
        for key in city_request:
            if key != "id" and key != "created_at" and key != "updated_at":
                if key != 'state_id':
                    city_upd[key] = city_request[key]
        storage.save()
        return jsonify(city_upd.to_dict()), 200
    except:
        abort(400, "Not a JSON")
