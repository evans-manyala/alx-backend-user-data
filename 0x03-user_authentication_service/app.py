#!/usr/bin/env python3
"""
Basic Flask App
"""

import os
from typing import Tuple
from flask import Flask, abort, jsonify, request, redirect
from flask_cors import CORS
from auth import Auth
import utils
from werkzeug import Response

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """
    Handle GET requests to the root URL.

    Returns:
        Response: A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> Tuple[Response, int]:
    """
    Handle POST requests to the /users endpoint to register a new user.

    Returns:
        Tuple[jsonify, int]: A tuple containing the JSON response and
        the HTTP status code.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate input
    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Tuple[Response, int]:
    """
    Handle POST requests to the /sessions endpoint to log in a user.

    Returns:
        Tuple[jsonify, int]: A tuple containing the JSON response and
        the HTTP status code.
    """

    response, error_msgs = utils.request_body_provided(
        expected_fields={"email": str, "password": str}
    )
    if not response:
        return jsonify({"message": error_msgs}), 400

    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email=email, password=password):
        abort(401)

    session_id = AUTH.create_session(email=email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie(key="session_id", value=session_id)
    return response, 200


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Tuple[Response, int]:
    """
    DELETES requests to the /sessions endpoint to log out a user.

    Returns:
        Tuple[Response, int]: A tuple containing the response
        & HTTP status code.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        return jsonify({"message": "Invalid session ID"}), 403

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Tuple[Response, int]:
    """
    GET requests to the /profile endpoint to get user profile information.

    Returns:
        Tuple[Response, int]: A tuple containing the JSON response &
        the HTTP status code.
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)
    return jsonify({
        "email": user.email,
        "message": "Profile information retrieved successfully"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
