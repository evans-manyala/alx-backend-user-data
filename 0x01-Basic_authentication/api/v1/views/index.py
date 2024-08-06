#!/usr/bin/env python3
""" Module for Index Views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route("/unauthorized", methods=["GET"], strict_slashes=False)
def unauthorized() -> str:
    """
    GET /api/v1/unauthorized
    Simulate an unauthorized access scenario.
    - This endpoint raises a 401 Unauthorized error.
    """
    abort(401, description="Unauthorized")


@app_views.route("/forbidden", methods=["GET"], strict_slashes=False)
def forbidden() -> str:
    """
    GET /api/v1/forbidden
    Simulate a forbidden access scenario.
    - This endpoint raises a 403 Forbidden error.
    """
    abort(403, description="Forbidden")


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Check the status of the API.
    - Returns a JSON response with the status of the API as "OK".
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats/", strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Retrieve statistics about the number of objects.
    - Returns a JSON response with the count of users from the User model.
    """
    from models.user import User

    stats = {}
    stats["users"] = User.count()
    return jsonify(stats)
