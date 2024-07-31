#!/usr/bin/env python3
"""
Obfuscates specified fields in a log message.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    """
    pattern = "|".join(f"{field}=.*?(?={separator}|$)" for field in fields)
    return re.sub(pattern, lambda m:
                  f"{m.group().split('=')[0]}={redaction}", message)
