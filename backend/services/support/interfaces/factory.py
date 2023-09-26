"""Factory Interface
"""
from abc import ABCMeta, abstractmethod


class AppFactoryInterface(metaclass=ABCMeta):
    """Factory interface definition"""

    @abstractmethod
    def initialize_app(self):
        """
        Implement all exceptions
        """
