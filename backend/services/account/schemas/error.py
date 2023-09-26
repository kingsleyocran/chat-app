"""Errors Schema

This module contains the schemas for errors
"""
import pydantic


class UserNotFound(pydantic.BaseModel):
    """User Not Found Schema
    Attributes:
        error (str): error for the payload
    """

    error: str


class UnAuthorizedError(pydantic.BaseModel):
    """Unauthorized error Schema
    Attributes:
        error (str): error for the payload
    """

    error: str


class InvalidRefreshToken(pydantic.BaseModel):
    """Invalid Refresh Token Schema
    Attributes:
        error (str): error for the payload
    """

    error: str
