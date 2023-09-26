"""Users Schemas

This module contains all schemas relating to users
"""

from pydantic import BaseModel, EmailStr, validator
from utils import sql


class RegisterUser(BaseModel):
    """Register User Schema
    Attributes:
        email (str): email for the payload
        username (str): username for the payload
        password (str): password for the payload
    """

    username: str
    email: EmailStr
    password: str

    _check_username = validator("username", allow_reuse=True)(sql.check_sql_injection)

    class Config:
        orm_mode = True


class User(BaseModel):
    """User  Schema
    Attributes:
        email (str): email for the payload
        username (str): username for the payload
    """

    username: str
    email: EmailStr

    _check_username = validator("username", allow_reuse=True)(sql.check_sql_injection)

    class Config:
        orm_mode = True


class AdminUser(BaseModel):
    """Admin Schema

    Attributes:
        username (str): username to be admin
    """

    username: str

    _check_username = validator("username", allow_reuse=True)(sql.check_sql_injection)

    class Config:
        orm_mode = True


class ChangeEmail(BaseModel):
    """Change Email Schema
    Attributes:
        email (str): email for the payload
    """

    email: EmailStr


class ChangeUsername(BaseModel):
    """Change Username Schema
    Attributes:
        username (str): username for the payload
    """

    username: str
    _check_username = validator("username", allow_reuse=True)(sql.check_sql_injection)


class ChangePassword(BaseModel):
    """Change Password Schema
    Attributes:
        password (str): password for the payload

    """

    password: str


class ChangeOut(BaseModel):
    """Change Out Schema

    This schema is used for all
    return operations that involve
    change

    Note - Output Schema for change operations

    Attributes:
        message (str): message for the payload
    """

    message: str


class AdminOut(ChangeOut):
    """
    This schema is used for Admin

    Note - Output Schema for add Admin

    Attributes:
        password (str): password for the payload
    """

    password: str
