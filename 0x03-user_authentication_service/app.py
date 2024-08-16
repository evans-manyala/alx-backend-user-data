#!/usr/bin/env python3
"""
Basic Flask App
"""

from flask import (
    Flask,
    jsonify,
    request,
    abort,
    redirect,
    url_for,
    make_response,
    session
)
from flask_cors import CORS
from auth import Auth


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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Login a user and create a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)  # Incorrect login information

    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(401)  # Failed to create a session

    response = make_response(jsonify({
        "email": email,
        "message": "session created"
    }))
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
