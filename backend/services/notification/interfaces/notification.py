"""Interfaces for Controllers
"""

from abc import ABC, abstractmethod


class NotificationController(ABC):
    """Implement Email Controller Interface"""

    @abstractmethod
    def send(self):
        """Implement send functionality"""
