"""Sql Utility
Sql module to handle all sql operations
as a decorator or function
"""

import re
from functools import wraps
from typing import Any, Callable

from error import exceptions
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tools import log


def sql_error_handler(func: Callable[..., object]) -> Any:
    """
    Check the error of an sql operation
    Args:
        func (object): func to decorate
    Returns:
        func
    Raises:
        UserOperationsError: raises user operation error
        ServerError: raises server error
    """

    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            error_logger = log.Log(f"{func.__module__}.{func.__name__}")
            error_logger.exception(e.args[0])
            raise exceptions.UserOperationsError(msg="Username already exist")

        except Exception as e:
            error_logger = log.Log(f"{func.__module__}.{func.__name__}")
            error_logger.exception(e.args[0])
            raise exceptions.ServerError(msg="Error processing request")

    return inner


def add_object_to_database(db: Session, item: Any) -> bool:
    """
    Add an item to the database
    Args:
        db (object): contain the session for the
                database operations
        item(Any): The item to insert
    returns:
        bool
    """
    db.add(item)
    db.commit()
    db.refresh(item)
    return True


def check_sql_injection(value: str) -> str:
    """Perform validation on Username

    Verify if username is valid
    """
    pattern = r"^[a-z0-9\._@]+\Z"
    reg = re.compile(pattern)
    if not bool(reg.match(value)):
        raise ValueError(f"Invalid format {value} used")
    return value.lower()
