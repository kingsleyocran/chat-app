"""Builder Interface
"""

from abc import ABCMeta, abstractmethod


class AppBuilderInterface(metaclass=ABCMeta):
    """Builder Interface definition"""

    @abstractmethod
    def register_exceptions(self):
        """
        Implement all exceptions
        """

    @abstractmethod
    def register_middlewares(self):
        """
        Implement all middlewares
        """

    @abstractmethod
    def register_routes(self):
        """Implement all routes"""
