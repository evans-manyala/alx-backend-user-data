#!/usr/bin/env python3
"""
Hashed Password Utility module
"""

from db import DB
from user import User
from bcrypt import hashpw, gensalt


class Auth:
    """
    Authentication class
    """

    def __init__(self) -> None:
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        """
        Hashes a password using bcrypt
        """

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password

    def register_user(self, email, password):
        """
        Registers a new user with the given email and password
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email=email, hashed_password=hashed_password)
            return new_user