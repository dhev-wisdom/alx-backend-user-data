#!/usr/bin/env python3
"""
Module returns obfuscated log message
"""

import mysql.connector
import logging
from os import environ
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "ip")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format method to filter values in incoming log records
        using filter_datum
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


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
    for field in fields:
        message = re.sub(f"{field}=(.*?){seperator}",
                         f"{field}={redaction}{seperator}", message)
    return message


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object.
    """
    logger = logging.get_logger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_logger() -> logging.Logger:
    """ Returns a Logger Object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db():
    """
    function returns a connector to the database
    """
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    db_user = environ.get("PERSONAL_DATA_DB_USERNAME")
    db_pass = environ.get("PERSONAL_DATA_DB_PASSWORD")
    db_host = environ.get("PERSONAL_DATA_DB_HOST")

    connection = mysql.connector.connection.MySQLConnection(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
            )
    return connection
