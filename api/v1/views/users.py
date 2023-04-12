#!/usr/bin/python3
"""Endpoints for the User class."""
from flask import abort
from flask import jsonify
from flask import request
from api.v1.views import app_views
from models import storage
from console import classes


@app_views.route("/users", strict_slashes=False)
def get_all_users():
    """Return a list of all users."""
    users_list = [user.to_dict()
                  for user in storage.all(classes["User"]).values()]
    if users_list is not None:
        return jsonify(users_list)
    else:
        return jsonify([])


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user_by_id(user_id):
    """Return a User by its id."""
    all_amenity = storage.all(classes["User"])
    if f"User.{user_id}" in all_amenity:
        return jsonify(all_amenity[f"User.{user_id}"].to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a User object from the storage."""
    user_instance = storage.get(classes["User"], user_id)
    if user_instance:
        storage.delete(user_instance)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new User."""
    try:
        req = request.get_json()
        if "email" in req:
            if "password" in req:
                user_instance = classes["User"]()
                user_instance.email = req["email"]
                user_instance.password = req["password"]
                storage.new(user_instance)
                storage.save()
                return user_instance.to_dict(), 201
            else:
                abort(400, "Missing password")
        else:
            abort(400, "Missing email")
    except:
        abort(400, "Not a JSON")


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Update the atributes of a user instance."""
    user_instance = storage.get(classes["User"], user_id)
    if user_instance:
        try:
            req = request.get_json()
            for key, value in req.items():
                if (key != "id" and key != "created_at" and
                        key != "updated_at" and key != "email"):
                    setattr(user_instance, key, value)
            user_instance.save()
            return jsonify(user_instance.to_dict()), 200
        except:
            abort(400, "Not a JSON")
    else:
        abort(404)
