#!/usr/bin/env python3
"""
Hashed Password Utility module
"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(self, password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """

    hashed_password = password.encode('utf-8')
    return bcrypt.hashpw(hashed_password, bcrypt.gensalt())


class Auth:
    """
    Authentication class
    """

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashed_password)
            return new_user
