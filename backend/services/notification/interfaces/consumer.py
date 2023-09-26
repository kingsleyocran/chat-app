"""Interfaces for Consumers
"""

from abc import ABC, abstractmethod


class NotificationConsumer(ABC):
    """Implement Notification Consumer Interface"""

    @abstractmethod
    def consume(self):
        """Implement consume functionality"""
