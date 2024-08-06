#!/usr/bin/env python3
"""
Definition of class Auth
"""
from flask import request
from typing import List, Optional, TypeVar


class Auth:
    """
    Manages the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if a given path requires authentication.

        Args:
            path (str): URL path to be checked.
            excluded_paths (List[str]): List of paths that
            do not require authentication.

        Returns:
            bool: True if the path requires authentication,
            False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        normalized_path = path if path.endswith("/") else path + "/"

        for excluded_path in excluded_paths:
            normalized_excluded_path = (
                excluded_path if excluded_path.endswith("/")
                else excluded_path + "/"
            )

        if normalized_path.startswith(normalized_excluded_path):
            return False
        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """
        Get the authorization header from the request object.

        Args:
            request: The incoming request object.

        Returns:
            Optional[str]: The value of the 'Authorization'
            header if present, otherwise None.
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieve a User instance based on information from the request object.

        Args:
            request: The incoming request object.

        Returns:
            TypeVar('User'): An instance of User if authentication
            is successful, otherwise None.
        """
        return None
