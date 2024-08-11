#!/usr/bin/env python3

"""
Session Authentication Module For Views
"""

import os
from typing import Tuple

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    POST /api/v1/auth_session/login

    Return:
        JSON representation of a User object.
    """

    not_found_res = {"error": "no user found for this email"}
    email = request.form.get("email")
    if not email or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if not password or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search(email)
    except Exception as e:
        # Consider logging the exception e
        return jsonify(not_found_res), 404

    if not users:
        return jsonify(not_found_res), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth

        session_id = auth.create_session(users[0].id)
        result = jsonify(users[0].to_json())
        result.set_cookie(os.getenv("SESSION_NAME", "_my_session_id"),
                          session_id)
        return result

    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout() -> Tuple[str, int]:
    """
    DELETE /api/v1/auth_session/logout

    Return:
        An empty JSON object.
    """

    from api.v1.app import auth

    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)

    return jsonify({})
