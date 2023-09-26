"""Model Utility
Model module to handle all model error operations
as a decorator or function
"""

from functools import wraps

from error import exceptions
from utils import log


def model_error_handler(func: object) -> object:
    """
    Check the error of an model operation
    Args:
        func (object): func to decorate
    Returns:
        func
    Raises:
        ModelError: raises model operation error
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            error_logger = log.Log(f"{func.__module__}.{func.__name__}")
            error_logger.exception(e.args[0])
            raise exceptions.ModelError(msg="Error processing request")

    return inner
