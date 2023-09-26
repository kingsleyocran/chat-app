"""Model Interface
"""

from abc import ABCMeta, abstractmethod


class DaveModelInterface(metaclass=ABCMeta):
    """Model Interface definition"""

    @abstractmethod
    def reply(self):
        """
        Implement model functinality
        """
