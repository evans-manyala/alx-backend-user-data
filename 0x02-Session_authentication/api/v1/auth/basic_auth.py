#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
import base64
from .auth import Auth
from typing import TypeVar, Tuple, Optional

from models.user import User


class BasicAuth(Auth):
    """Basic Authorization protocol implementation"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> Optional[str]:
        """
        Extract the Base64-encoded token from the Authorization header.

        Args:
            authorization_header (str): The Authorization header
            from the request.

        Returns:
            Optional[str]: The Base64-encoded token if the header
            is valid, otherwise None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        token = authorization_header.split(" ")[-1]
        return token

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> Optional[str]:
        """
        Decode a Base64-encoded string.

        Args:
            base64_authorization_header (str): Base64-encoded string to decode.

        Returns:
            Optional[str]: The decoded string if successful, otherwise None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header.encode
                                       ("utf-8"))
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract the email and password from a Base64-decoded string.

        Args:
            decoded_base64_authorization_header (str): Base64-decoded string
            containing credentials.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing the
            email and password if valid, otherwise (None, None).
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        email, passwd = decoded_base64_authorization_header.split(":", 1)
        return (email, passwd)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> Optional[TypeVar("User")]:
        """
        Retrieve a User instance based on email and passwd.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's passwd.

        Returns:
            Optional[TypeVar('User')]: A User instance if credentials
            are valid, otherwise None.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            for u in users:
                if u.is_valid_passwd(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> Optional[TypeVar("User")]:
        """
        Retrieve a User instance from the request based on the
        Authorization header.

        Args:
            request: The incoming request object.

        Returns:
            Optional[TypeVar('User')]: A User instance if credentials
            are valid, otherwise None.
        """
        auth_header = self.authorization_header(request)
        if auth_header:
            token = self.extract_base64_authorization_header(auth_header)
            if token:
                decoded = self.decode_base64_authorization_header(token)
                if decoded:
                    email, passwd = self.extract_user_credentials(decoded)
                    if email:
                        return self.user_object_from_credentials(email, passwd)
        return None
