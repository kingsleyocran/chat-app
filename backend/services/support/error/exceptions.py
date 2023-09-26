"""Exceptions

This module contains the various operation
exceptions that may occur
"""


class BaseException(Exception):
    """Base Exception

    Attributes:
        msg (str): Exception message
        status_code (int): status_code
    """

    def __init__(self, msg, status_code=400):
        """Construct an exception

        Args:
            msg (str): message to be used
            status_code (int): status code
        """
        self.msg = msg
        self.status_code = status_code


class ModelError(BaseException):
    """Model Operation error"""
