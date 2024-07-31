#!/usr/bin/env python3
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
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
    pattern = "|".join(f"{field}=.*?(?={separator}|$)" for field in fields)
    return re.sub(pattern, lambda m:
                  f"{m.group().split('=')[0]}={redaction}", message)
