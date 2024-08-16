#!/usr/bin/env python3
"""
Hashed Password Utility module
"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


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
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password).decode()
            return self._db.add_user(email=email,
                                     hashed_password=hashed_password)

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

        return bcrypt.checkpw(password.encode("utf-8"),
                              user.hashed_password.encode("utf-8"))

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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieve a user based on the given session ID.

        Args:
            session_id (str): The session ID used to identify the user.

        Returns:
                The user object if found, otherwise None.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user session by setting their session ID to None.

        Args:
            user_id (int): The ID of the user session.

        Returns:
            None
        """
        try:
            self._db.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"{user_id} is not a valid user ID.")
        self._db.update_user(user_id=user_id, session_id=None)
