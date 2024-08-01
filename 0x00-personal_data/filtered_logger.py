#!/usr/bin/env python3
"""
Obfuscates specified fields in a log message.
"""
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscates specified fields in a log message.
    """
    pattern = "|".join(f"{field}=.*?(?={separator}|$)" for field in fields)
    return re.sub(pattern, lambda m:
                  f"{m.group().split('=')[0]}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

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
        return filter_datum(self.fields, self.REDACTION,
                            original_msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates a logger named 'user_data' with INFO level
    and a StreamHandler that uses RedactingFormatter
    to obfuscate PII fields.
    """

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database using
    credentials from environment variables.
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user,
                                   password=passwd,
                                   host=host,
                                   database=db_name)
    return conn