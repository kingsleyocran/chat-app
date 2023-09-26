"""User Operations Interface
"""
from abc import ABC, abstractmethod


class UserOperationsInterface(ABC):
    """User Operations Interface defintion"""

    @abstractmethod
    def register_user(self):
        """Implement register user"""

    @abstractmethod
    def verify_user(self):
        """Implment verify user"""
