#!/usr/bin/env python3
"""
Hashed Password Utility module
"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """

    hashed_password = password.encode('utf-8')
    return bcrypt.hashpw(hashed_password, bcrypt.gensalt())
