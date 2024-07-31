#!/usr/bin/env python3
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 pattern: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): String to replace field values with.
        message (str): The log line to be processed.
        separator (str): Character that separates
        fields in the log line.

    Returns:
        str: The log line with specified fields obfuscated.
    """
    for field in fields:
        pattern = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', pattern)
    return pattern
