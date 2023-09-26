"""Add Admin Consumer in the system

This module demonstrates how to consume or
subscribe to a particular topic and the operation
performed on that topic, mainly add admin topic

Attributes:
    app_settings (object): Application Settings
    consumer_logger (object): Logger instance
    count (object): Counts the messages sent
"""

import asyncio
import json

from aiokafka import AIOKafkaConsumer

from config import settings
from interfaces import consumer
from interfaces import notification as nt
from plugins import grafana
from tools import log

app_settings = settings.Settings()

consumer_logger = log.Log(__file__)


class AddAdminConsumer(consumer.NotificationConsumer):
    """Consumer for Add Admin in the System

    This class describes the operations performed
    for admins that just joined the system
    """

    @staticmethod
    async def consume(consume_with: nt.NotificationController = None):
        """Listen to a particular topic

        Args:
            consume_with (class): The operation controller
                The controller to use when you are listening
                to a particular topic
        """
        consumer = AIOKafkaConsumer(
            app_settings.topic_for_admin,
            bootstrap_servers=app_settings.broker_url,
            group_id="admins",
        )

        await consumer.start()
        try:
            async for msg in consumer:
                payload = json.loads(msg.value)
                username = payload.get("username")
                user_email = payload.get("email")
                password = payload.get("password")

                if consume_with is not None:
                    consume_with.send(username, user_email, password)

        except Exception as e:
            consumer_logger.exception(e.args[0])

        finally:
            await consumer.stop()

    @staticmethod
    def start_process():
        """Start the consumer process"""
        grafana_controller = grafana.Grafana()
        asyncio.run(AddAdminConsumer.consume(consume_with=grafana_controller))
