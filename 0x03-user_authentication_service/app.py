#!/usr/bin/env python3
"""
Basic Flask App
"""

import os
from typing import Tuple
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from auth import Auth
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
def users() -> Tuple[jsonify, int]:
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
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
