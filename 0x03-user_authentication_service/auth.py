#!/usr/bin/env python3
"""
Hashed Password Utility module
"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union, Tuple


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """
    Generates a new UUID
    """
    return str(uuid4())


class Auth:
    """
    Authentication class
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password
        """
        if not email:
            raise ValueError("Email cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")

        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            pass

        else:
            raise ValueError("User already exists")

        hashed_password = _hash_password(password=password).decode()
        return self._db.add_user(email=email, hashed_password=hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login credentials

        Args:
            email (str): user's email address
            password (str): user's password
        Return:
            True if credentials are correct, else False
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        passwd_ = password.encode("utf-8")
        return bcrypt.checkpw(passwd_, user_password)

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creates a new session for the user with the given email.

        Args:
            email (str): The user's email.

        Returns:
            str | None: The new session ID if the user is found,
            None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
