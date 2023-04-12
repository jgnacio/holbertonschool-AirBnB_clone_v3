#!/usr/bin/python3
"""Endpoints for the state class."""
from flask import abort
from flask import jsonify
from flask import request
from api.v1.views import app_views
from models import storage
from console import classes


@app_views.route("/states", strict_slashes=False)
def get_all_states():
    """Return a list of all states."""
    states_list = [state.to_dict()
                   for state in storage.all(classes.get("State", 0)).values()]
    if states_list is not None:
        return jsonify(states_list)
    else:
        return jsonify([])


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state_by_id(state_id):
    """Return a state by its id."""
    all_state = storage.all(classes["State"])
    if f"State.{state_id}" in all_state:
        return jsonify(all_state[f"State.{state_id}"].to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object from the storage."""
    obj_to_delete = storage.get(classes["State"], state_id)
    if obj_to_delete:
        storage.delete(obj_to_delete)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a new state."""
    try:
        req = request.get_json()
        if "name" in req:
            state_instance = classes["State"]()
            state_instance.name = req["name"]
            storage.new(state_instance)
            storage.save()
            return state_instance.to_dict(), 201
        else:
            abort(400, "Missing name")
    except:
        abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update the atributes of a state instance."""
    state_instance = storage.get(classes["State"], state_id)
    if state_instance:
        try:
            req = request.get_json()
            for key, value in req.items():
                if key != "id" and key != "created_at" and key != "updated_at":
                    setattr(state_instance, key, value)
            state_instance.save()
            return jsonify(state_instance.to_dict()), 200
        except:
            abort(400, "Not a JSON")
    else:
        abort(404)
