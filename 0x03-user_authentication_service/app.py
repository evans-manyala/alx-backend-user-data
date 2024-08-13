#!/usr/bin/env python3
"""
Basic Flask App
"""

from flask import Flask, jsonify
from auth import Auth
from flask import request

AUTH = Auth()


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    Handle GET requests to the root URL
    Returns:
        Response: A JSON response with a message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """
    Handle POST requests to the /users URL
    Returns:
        Response: A JSON response with a message
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or password:
        return jsonify({"error": "Email and password are required"}), 400
    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message":
                        "User created successfully"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
