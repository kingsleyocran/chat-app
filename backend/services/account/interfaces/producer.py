"""Producer Interface
"""

from abc import ABCMeta, abstractmethod


class ProducerInterface(metaclass=ABCMeta):
    """Producer Interface definition"""

    @abstractmethod
    def send_message(self, action: str, message: str):
        """
        Implement send message
        """
