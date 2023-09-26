"""Grafana Plugin

This module demonstrates how to add users
to grafana database

Attributes:
    app_settings (object): Application Settings
    grafana_logger (object): Logger instance
"""

import base64

import requests
from config import settings
from interfaces import notification
from tools import log

app_settings = settings.Settings()

grafana_logger = log.Log(__file__)


class Grafana(notification.NotificationController):
    """Grafana Controller

    This consist of the operations to insert data
    through grafana API
    """

    def __init__(self) -> None:
        self._ADD_USER_URL = "/api/admin/users"
        self._END_POINT = app_settings.grafana_server_url + self._ADD_USER_URL

    def _generate_base64_string(self, user: str, password: str) -> str:
        """
        Generate Base64 string from
        header authorization basic auth credentials
        """
        value_bytes = base64.b64encode(f"{user}:{password}".encode("utf-8"))
        return value_bytes.decode("ascii")

    def send(self, username: str, email: str, password: str) -> bool:
        """Send a request to grafana

        This method is to insert a user to grafana

        Raises:
            Exception: Exception when something occurs
        Returns:
            bool : True is successful, False otherwise
        """
        try:
            auth = self._generate_base64_string(
                user=app_settings.grafana_admin_user,
                password=app_settings.grafana_admin_password,
            )
            headers = {
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json",
            }
            response = requests.post(
                url=self._END_POINT,
                headers=headers,
                json={
                    "name": username,
                    "email": email,
                    "login": username,
                    "password": password,
                    "OrgId": 1,
                },
            )
            if response.status_code == 200:
                grafana_logger.info(f"{username} added to grafana")
                return True
            grafana_logger.error(f"{response.text}")
        except Exception as e:
            grafana_logger.exception(e.args[0])
