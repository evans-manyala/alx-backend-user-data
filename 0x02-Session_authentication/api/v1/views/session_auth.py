#!/usr/bin/env python3
"""
Session Authentication Views
"""
from flask import Blueprint, request, jsonify, abort, make_response
from models.user import User
import os

app_views = Blueprint("session_auth", __name__)


@app_views.route("/auth_session/login/", methods=["POST"], strict_slashes=False)
@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """
    POST /api/v1/auth_session/login
    Create a session for a user.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Check email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve User instance based on email
    user = User.search(email)
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404

    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session ID
    from api.v1.app import auth  # Import here to avoid circular import

    session_id = auth.create_session(user.id)

    # Create response
    response = jsonify(user.to_json())
    session_name = os.getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)

    return response
