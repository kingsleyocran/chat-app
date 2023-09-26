import secrets

from config import setting

app_settings = setting.AppSettings()


def generate_password() -> str:
    length = app_settings.AUTO_PASSWORD_LENGTH
    password = secrets.token_hex(length)
    return password
