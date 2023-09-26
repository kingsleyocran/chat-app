"""General Application Settings

This module stores all the configurations
for the application
"""
import pydantic


class AppSettings(pydantic.BaseSettings):
    """Application Settings
    Attributes:
            DATABASE_URL (str) : Production database url
            TEST_DATABASE_URL (str): Test database url
            TESTING (bool): Test or Production environment
            LOG_FILENAME (str): Log file name
            API_PREFIX (str): API router prefix name
            authjwt_secret_key (str): Secret key for access token
            authjwt_access_token_expires (int): Expiration of the access token
            authjwt_refresh_token_expires (int): Expiration of refresh token
            authjwt_access_cookie_key (str): Secret key for cookie access token
            authjwt_refresh_cookie_key (str): key for cookie refresh token
            authjwt_denylist_enabled (bool): Allow deny list enabled
            authjwt_denylist_token_checks (set): Tokens to check for deny list
            REDIS_HOST (str): The host name of the redis
            REDIS_PORT (int): The port number of the redis
            REDIS_PASSWORD(str): The password for redis
            APP_TITLE (str): Application title
            APP_DESCRIPTION (str): Application description
            BROKER_URL (str): Kafka broker to connect to
            ADMIN_USERNAME (str): The administrator username
            ADMIN_PASSWORD (str): The administrator password
            ADMIN_EMAIL (str): The administrator email
            AUTO_PASSWORD_LENGTH (int): length of auto password
    """

    DATABASE_URL: str
    TEST_DATABASE_URL: str
    TESTING: bool
    LOG_FILENAME: str
    API_PREFIX: str = "/api/v1"
    authjwt_secret_key: str
    authjwt_access_token_expires: int
    authjwt_refresh_token_expires: int
    authjwt_access_cookie_key: str
    authjwt_refresh_cookie_key: str
    authjwt_access_csrf_cookie_key: str
    authjwt_refresh_csrf_cookie_key: str
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    APP_TITLE: str = "Chat Application"
    APP_DESCRIPTION: str = "Management service for chat application"
    BROKER_URL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_EMAIL: str
    AUTO_PASSWORD_LENGTH: int = 23

    class Config:
        """Meta configuration"""

        env_file = ".env"
