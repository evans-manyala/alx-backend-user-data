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
