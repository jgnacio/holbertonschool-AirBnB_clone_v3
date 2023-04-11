#!/usr/bin/python3
"""This module provides a simple get status of the web server."""
from api.v1.views import app_views
from models import storage
from console import classes


@app_views.route("/status", strict_slashes=False)
def status():
    """Return OK status."""
    return {"status": "OK"}


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Get the number of instances of each class."""
    stats_dict = {
        "amenities": classes.get("Amenity", 0),
        "cities": classes.get("City", 0),
        "places": classes.get("Place", 0),
        "reviews": classes.get("Review", 0),
        "states": classes.get("State", 0),
        "users": classes.get("User", 0)
    }
    stats_dict = {cls_key: storage.count(cls_obj) for cls_key,
                  cls_obj in stats_dict.items()}

    return stats_dict
