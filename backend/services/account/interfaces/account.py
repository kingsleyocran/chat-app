"""Account Interface
"""

from abc import ABC, abstractmethod


class AccountOperationsInterface(ABC):
    """Account definition"""

    @abstractmethod
    def create_account(self):
        pass
