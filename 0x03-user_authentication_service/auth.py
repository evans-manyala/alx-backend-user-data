#!/usr/bin/env python3
"""
Hashed Password Utility module
"""


import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """

    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_passwd
