#!/usr/bin/env python3
"""
Module returns obfuscated log message
"""

import logging
import re
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        seperator: str
        ) -> str:
    """
    Function returns the log message obfuscated

    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string character is separating all fields in the message

    Return:
        log messsage (message)
    """
    password_pattern = r"password([^;]+;)"
    dob_pattern = r"date_of_birth([^;]+;)"
    message_ = re.sub(password_pattern, f"password={redaction};", message)
    message_ = re.sub(dob_pattern, f"date_of_birth={redaction};", message_)
    return message_
