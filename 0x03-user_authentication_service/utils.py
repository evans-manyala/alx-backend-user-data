#!/usr/bin/env python3
"""
Utilities module for handling request validation in the Flask app.

This module provides functions to ensure that all required form data fields
are present in the request body before processing the request. It helps
in standardizing the validation process across different endpoints.
"""

from typing import Any, Tuple, Union
from flask import request


def _check_form_data_field_existence(*, expected_fields: set) -> None:
    """
    Internal helper function to verify the presence of expected fields in the
    request body.

    This function checks if the provided `expected_fields` are present in the
    incoming request's form data. If the request body does not contain the
    required fields, it raises a ValueError with an appropriate message.

    Args:
        expected_fields (set): A set of field names expected to be in
        the request body.

    Raises:
        ValueError: If the request body is empty or if any expected
        field is missing.
    """
    if not request.form:
        raise ValueError({"expected_fields": list(expected_fields)})
    for field in expected_fields:
        if not request.form.get(field):
            raise ValueError(f"{field} missing")


def request_body_provided(
    *, expected_fields: set
) -> Union[Tuple[bool, Any], Tuple[bool, None]]:
    """
    Validate the presence of required fields in the request body.


    Args:
        expected_fields (set): A set of field names expected to be in the
        request body.

    Returns:
        Tuple[bool, Any]: A tuple where the first element is a boolean
        indicating success (`True`) or failure (`False`), and the second
        element is either `None` (on success) or an error message (on failure).
    """
    try:
        _check_form_data_field_existence(expected_fields=expected_fields)
    except ValueError as err:
        return False, err.args[0]

    return True, None
