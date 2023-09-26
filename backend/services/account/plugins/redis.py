"""Redis Plugin

This module handles all operations
for redis

Attributes:
    settings (object): Application settings
"""

import redis
from config import setting

settings = setting.AppSettings()


class DenyListStorage:
    """Deny List Memory Storage

    This class is responsible for
    storing revoked tokens

    Attributes:
        _redis_server (object): Redis configured object
    """

    def __init__(self) -> None:
        """Construct a Deny list storage instance"""
        self._redis_server = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=0,
            decode_responses=True,
        )

    def set_value(self, key: str, value) -> None:
        """Set value

        This method sets a key and value pair to
        the deny list storage database
        """
        self._redis_server.set(
            name=key, value=value, ex=settings.authjwt_access_token_expires
        )

    def get_value(self, key: str) -> str:
        """Get value

        This method returns the value from
        the deny list storage database

        Args:
            key (str): item key value
        Returns:
            str : result from the deny storage
        """
        result = self._redis_server.get(key)
        return result
