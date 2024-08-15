#!/usr/bin/env python3
"""
Hashed Password Utility module
"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


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
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {existing_user.email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashed_password)
        return new_user

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

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user with the given email.

        Args:
            email (str): The user's email.

        Returns:
            str: The new session ID.

        Raises:
            ValueError: If the user with the given email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db.session.commit()
            return session_id
        except NoResultFound:
            raise ValueError("User not found")
