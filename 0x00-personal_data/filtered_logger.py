#!/usr/bin/env python3
"""
Obfuscates specified fields in a log message.
"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    """
    pattern = "|".join(f"{field}=.*?(?={separator}|$)" for field in fields)
    return re.sub(pattern, lambda m:
                  f"{m.group().split('=')[0]}={redaction}", message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by obfuscating specified fields.
        """
        original_msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, original_msg, self.SEPARATOR)
