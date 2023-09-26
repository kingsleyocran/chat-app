"""New users Consumers in the system

This module demonstrates how to subscribe to
a particular topic and the operation performed
on that topic, mainly new users topic

Attributes:
    app_settings (object): Application Settings
    consumer_logger (object): Logger instance
    CLICK_URL (str): Url for verified account
    count (object): Counts the messages sent
"""

import asyncio
import json

from aiokafka import AIOKafkaConsumer
from config import settings
from interfaces import consumer
from interfaces import notification as nt
from plugins import mail
from tools import log

app_settings = settings.Settings()

consumer_logger = log.Log(__file__)

CLICK_URL = f"{app_settings.auth_service_url}/api/v1/verify/account"


class NewUsersConsumer(consumer.NotificationConsumer):
    """Consumer for New Users in the System

    This class describes the operations performed
    for users that just joined the system
    """

    @staticmethod
    async def consume(consume_with: nt.NotificationController = None) -> None:
        """Listen to a particular topic

        Args:
            consume_with (class): The operation controller
                The controller to use when you are listening
                to a particular topic
        """
        consumer = AIOKafkaConsumer(
            app_settings.topic_for_new_users,
            bootstrap_servers=app_settings.broker_url,
            group_id="users",
        )

        await consumer.start()
        try:
            async for msg in consumer:
                payload = json.loads(msg.value)
                username = payload.get("username")
                user_email = payload.get("email")
                token = payload.get("token")
                subject = "Welcome to Chat App"
                message = (
                    "Welcome to our Chat App Platform,"
                    f"Hello, {str(username).capitalize()}, \n\n"
                    "Click on this link to verify your email \n"
                    f"{CLICK_URL}?token={token}"
                )
                if consume_with is not None:
                    consume_with.send(subject, user_email, message)

        except Exception as e:
            consumer_logger.exception(e.args[0])

        finally:
            await consumer.stop()

    @staticmethod
    def start_process() -> None:
        """Start the consumer process"""
        email_controller = mail.Email()
        asyncio.run(NewUsersConsumer.consume(consume_with=email_controller))
