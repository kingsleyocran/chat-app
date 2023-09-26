"""Authentication Service

This module demonstrates how to authenticate a
user in the system

Attributes:
        settings (object): Application settings
            Defines the fields for running
            the application
"""
from datetime import timedelta

from fastapi import security
from fastapi_jwt_auth import AuthJWT

from config import setting
from plugins import redis

"""
# Use this for local memory
# denylist = set()c
# add - to add
# in - to search if jti exists
# Example:
#    jti in denylist
# """

settings = setting.AppSettings()


@AuthJWT.load_config
def get_config() -> setting.AppSettings:
    """Configuration settings for auth

    Returns:
        object: Auth configuration
    """
    settings.authjwt_access_token_expires = timedelta(
        minutes=settings.authjwt_access_token_expires
    )
    settings.authjwt_refresh_token_expires = timedelta(
        minutes=settings.authjwt_refresh_token_expires
    )
    return settings


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    """Check if your token has been revoked

    This function blacklists all user tokens
    especially when they log out

    Returns:
        bool: True is successful or false otherwise
    """
    jti = decrypted_token["jti"]
    token_id_found = redis_connection.get_value(jti)
    return token_id_found and token_id_found == "true"


Auth = AuthJWT
redis_connection = redis.DenyListStorage()
bearerschema = security.HTTPBearer()
