"""Account Schemas

This module contains all schemas related to account
"""
from pydantic import BaseModel, EmailStr, validator
from utils import sql


class CreateAccount(BaseModel):
    """Create Account Schema
    Attributes:
        email (str): email for the payload
        username (str): username for the payload
        profile_pic (str): profile_pic for the payload
    """

    email: EmailStr
    username: str
    profile_pic: str

    _check_username = validator("username", allow_reuse=True)(sql.check_sql_injection)

    class Config:
        orm_mode = True


class Login(BaseModel):
    """Login schema
    Attributes:
        email (str): email for the payload
        password (str): password for the payload
    """

    username: str
    password: str

    _check_username = validator("username", allow_reuse=True)(sql.check_sql_injection)

    class Config:
        orm_mode = True


class LoginOut(BaseModel):
    """LoginOut Schema

    This schema as an output schema
    for login operations
    Attributes:
        access_token (str): access_token for the payload
        refresh_token (str): refresh for the payload
    """

    access_token: str
    refresh_token: str
