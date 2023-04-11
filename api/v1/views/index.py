#!/usr/bin/python3
"""This module provides a simple get status of the web server."""
from api.v1.views import app_views

@app_views.route("/status", strict_slashes=False)
def status():
    """Return OK status."""
    return {"status": "OK"}
