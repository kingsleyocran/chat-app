"""Utility for perform user account operations

This module demonstrates the various operations that a user
of a system is allowed to person
"""
from datetime import datetime

from sqlalchemy import orm

from error import exceptions
from interfaces import account as acc_interface
from models import account as acc_model
from utils import sql


class AccountOperations(acc_interface.AccountOperationsInterface):
    """Account operations

    Contains the user operations or functions a user can perfom

    Attributes:
            _db (object): Database session
                For performing db operations on the database
    """

    def __init__(self, db: orm.Session):
        self._db = db

    @sql.sql_error_handler
    def create_account(self, user_id: int) -> None:
        """Create an Account for a User
        Args:
            user_id (int):  Id of the User to create
            the account for
        Raises:
            OperationError: sql Error
        """
        new_account = acc_model.UserAccount(user_id=user_id)
        sql.add_object_to_database(self._db, new_account)

    def get_account_with_user_id(self, user_id: int) -> acc_model.UserAccount:
        """Get an Account with a specific user id
        Args:
            user_id(int): Id of the User

        Raises:
            AccountOperationsError: raises an account operations error

        Returns:
            object: a user model instance

        """
        user_account = (
            self._db.query(acc_model.UserAccount)
            .filter(acc_model.UserAccount.user_id == user_id)  # type: ignore
            .first()
        )
        if user_account is None:
            raise exceptions.AccountOperationsError(
                "User Account not found", status_code=401
            )
        return user_account

    @sql.sql_error_handler
    def set_account_as_active(self, user_id: int) -> None:
        """Set User Account as Active in the system
        Args:
            user_id (int): Id of the user

        Raises:
            OperationError: sql Error
        """
        user_account = self.get_account_with_user_id(user_id)
        user_account.is_active = True
        user_account.updated_at = datetime.now()
        sql.add_object_to_database(self._db, user_account)

    @sql.sql_error_handler
    def set_account_as_inactive(self, user_id: int) -> None:
        """Set User Account as Inactive in the system
        Args:
            user_id (int): Id of the user
        Raises:
            OperationError: sql Error
        """
        user_account = self.get_account_with_user_id(user_id)
        user_account.is_active = False
        user_account.updated_at = datetime.now()
        sql.add_object_to_database(self._db, user_account)

    @sql.sql_error_handler
    def set_account_profile_pic(self, user_id: int, profile_pic: str) -> None:
        """Change the User Account profile picture in the system
        Args:
            user_id (int): Id of the user
            profile_pic(str): Profile picture image
            string for the user
        Raises:
            OperationError: sql Error
        """
        user_account = self.get_account_with_user_id(user_id)
        user_account.profile_pic = profile_pic
        sql.add_object_to_database(self._db, user_account)

    def is_user_account_active(self, user_id: int) -> bool:
        """Checks if a User account is active
        Args:
            user_id (int): Id of the user
        """
        user_account = self.get_account_with_user_id(user_id)
        account_state: bool = user_account.is_active
        return account_state
