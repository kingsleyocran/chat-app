"""Register all Producers in the system

This module demonstrates how a list of producers
send to a particular message on a topic

Attributes:
    app_settings (object): Application Settings
    consumer_logger (object): Logger instance
"""

import asyncio
import json
from typing import Any

from aiokafka import AIOKafkaProducer

from config import setting
from interfaces import producer
from tools import log

settings = setting.AppSettings()


producer_logger = log.Log(__file__)


class Producer(producer.ProducerInterface):
    """Producer for the kafka Service in the System

    This class describes the operations performed
    for users that just joined the system
    """

    async def _send_workload_to_kafka(self) -> None:
        """Send an action based on topics with a message"""
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.BROKER_URL,
        )

        await producer.start()
        try:
            data = json.dumps(self._message)
            await producer.send_and_wait(self._action, data.encode("utf-8"))
        except Exception as e:
            producer_logger.exception(e.args[0])
        finally:
            await producer.stop()

    def send_message(self, action: str, message: dict[Any, Any]) -> bool:
        """Start the producer process
        Attributes:
            _action (str): An action to perform or topic
            _message (str): The message to send with the action

         Args:
            action (str): An action to perform or topic
            message (str): The message to send with the action
        """
        self._message = message
        self._action = action
        asyncio.create_task(self._send_workload_to_kafka())
