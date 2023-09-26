"""Mail Plugin

This module demonstrates how to setup and
send an email message to a user

Attributes:
    app_settings (object): Application Settings
    email_logger (object): Logger instance
"""


import smtplib
import ssl
from email.mime import multipart, text
from typing import Any

from config import settings
from interfaces import notification
from tools import log

app_settings = settings.Settings()

email_logger = log.Log(__file__)


class Email(notification.NotificationController):
    """Email Controller

    This consist of the operations to send and email
    """

    def __init__(self) -> None:
        self._context = ssl.create_default_context()

    def _process_email(self, subject: str, recipient: str) -> Any:
        """Process email initial stages of the email body

        Returns:
            object
        """
        message = multipart.MIMEMultipart()
        message["Subject"] = subject
        message["From"] = app_settings.sender_email
        message["To"] = recipient
        return message

    def send(
        self, subject: str, recipient: str, message: str, html: str = None
    ) -> bool:
        """Send an email

        This method is for sending email messages

        Args:
            subject (str): Subject of the email body
            recipient (str): recipient of the email message
            message (str): message of the email body
            html (str): custom html format to send
        Raises:
            Exception: Exception when something occurs
        Returns:
            bool : True is successful, False otherwise
        """
        try:
            formatted_message = self._process_email(subject, recipient)

            if html is not None:
                serialize_html = text.MIMEText(html)
                formatted_message.attach(serialize_html, "html")

            if message is not None:
                serialize_text = text.MIMEText(message, "plain")
                formatted_message.attach(serialize_text)
                with smtplib.SMTP_SSL(
                    host=app_settings.stmp_server,
                    port=app_settings.email_port,
                    context=self._context,
                ) as email_server:
                    email_server.login(
                        user=app_settings.sender_email,  # type: ignore
                        password=app_settings.email_password,
                    )
                    email_server.sendmail(
                        app_settings.sender_email,
                        recipient,  # type : ignore
                        formatted_message.as_string(),
                    )
                email_logger.info(f"send email to the {recipient}")
            return True
        except Exception as e:
            email_logger.exception(e.args[0])
