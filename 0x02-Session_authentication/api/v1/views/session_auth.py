#!/usr/bin/env python3

"""
Session Authentication Module For Views
"""

import os
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth_session():
    """
    Handle user login.
    Return:
        JSON representation of user if found; else, error message.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search(email)
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth

            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv("SESSION_NAME", "_my_session_id")
            resp.set_cookie(session_name, session_id)
            return resp

    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def handle_logout():
    """
    Handle user logout.
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
