from pydantic import BaseSettings


class Settings(BaseSettings):
    VERSION: str = "0.1"
    API_PREFIX: str = "/api/v1"
    APP_TITLE: str = "Support Service"
    APP_DESCRIPTION: str = "This is an AI model based application"
    LOG_FILENAME: str = "chat_application.log"

    class Config:
        env_file = ".env"
