#!/usr/bin/env python3
"""
Basic Flask App
"""

import os
from flask import (
    Flask, abort, jsonify, redirect, request
)
from flask_cors import CORS
from auth import Auth
from typing import Tuple
# import utils


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
def users() -> str:
    """
    Handle POST requests to the /users endpoint to register a new user.

    Returns:
        Response: A JSON response indicating the result of the user
        registration.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate input
    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
