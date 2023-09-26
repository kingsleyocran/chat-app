"""Configuration for test

This module shows the configuration
done before you run a test

Attributes:
    SQLALCHEMY_DATABASE_URL (str): test database url
    engine (object): engine of the database
    SessionTesting (object): session of the database
"""
import os
import sys
from typing import Any, Generator

import pytest
from api.v1.router import account, users
from controller.account import AccountOperations
from controller.users import UserOperations
from core.setup import Base
from fastapi import FastAPI
from fastapi.testclient import TestClient
from schemas.users import RegisterUser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import sql
from utils.session import create

from . import test_data

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include backend dir in sys.path so that we can import from db,main.py
os.environ.setdefault("TESTING", "True")


def start_application():
    app = FastAPI()
    app.include_router(users.router)
    app.include_router(account.router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./testing_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[create] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def user_operations(db_session):
    return UserOperations(db_session)


@pytest.fixture(scope="function")
def account_operations(db_session):
    return AccountOperations(db_session)


@pytest.fixture(scope="function")
def already_registered_user(user_operations):
    registered_user_data = test_data.test_user_data
    test_user = RegisterUser(**registered_user_data)
    registered_user = user_operations.register_user(test_user)
    user_operations.set_email_as_verified(registered_user.id)
    return registered_user


@pytest.fixture(scope="function")
def already_registered_user_unverified(user_operations):
    registered_user_data = test_data.test_user_unverified
    test_user = RegisterUser(**registered_user_data)
    registered_user = user_operations.register_user(test_user)
    return registered_user


@pytest.fixture(scope="function")
def already_registered_admin(db_session, user_operations):
    registered_admin_data = test_data.test_admin_data
    test_user = RegisterUser(**registered_admin_data)
    registered_user = user_operations.register_user(test_user)
    user_operations.set_email_as_verified(registered_user.id)
    registered_user.is_admin = True
    sql.add_object_to_database(db_session, registered_user)
    return registered_user


@pytest.fixture(scope="function")
def already_created_account(account_operations, already_registered_user):
    account_operations.create_account(already_registered_user.id)
    account = account_operations.get_account_with_user_id(already_registered_user.id)
    return account


@pytest.fixture(scope="function")
def already_created_admin_account(account_operations, already_registered_admin):
    account_operations.create_account(already_registered_admin.id)
    account = account_operations.get_account_with_user_id(already_registered_admin.id)
    return account


@pytest.fixture(scope="function")
def already_logged_in_response(client, already_created_account):
    login_response = client.post("/login", json=test_data.test_login_data)
    return login_response


@pytest.fixture(scope="function")
def already_logged_in_admin_response(client, already_created_admin_account):
    login_response = client.post("/login", json=test_data.test_admin_login_data)
    return login_response
