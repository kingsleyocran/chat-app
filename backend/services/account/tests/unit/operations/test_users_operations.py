import pytest

from error import exceptions
from models.users import Users
from schemas.account import Login
from schemas.users import RegisterUser

from ... import test_data


@pytest.mark.user_operations
@pytest.mark.parametrize("register_user_data", [(test_data.test_user_data)])
def test_register_user(user_operations, register_user_data):
    test_user = RegisterUser(**register_user_data)
    saved_user = user_operations.register_user(test_user)

    # saved operations
    assert saved_user.username == test_user.username
    assert Users.verify_password(saved_user.hash_password, test_user.password)
    assert saved_user.email == test_user.email

    # user string representation
    assert str(saved_user) == f"{saved_user.id}-{saved_user.username}"


@pytest.mark.user_operations
@pytest.mark.parametrize("login_data", [(test_data.test_login_data)])
def test_verify_user(user_operations, already_registered_user, login_data):
    login_user_scheme = Login(**login_data)
    user_operations.set_email_as_verified(already_registered_user.id)
    login_user_id = user_operations.verify_user(login_user_scheme)
    assert login_user_id == already_registered_user.id


@pytest.mark.user_operations
def test_get_user_by_username(user_operations, already_registered_user):
    get_user_if_user_exists = user_operations.get_user_by(
        already_registered_user.username
    )
    assert get_user_if_user_exists.username == already_registered_user.username


@pytest.mark.user_operations
def test_get_user_by_id(user_operations, already_registered_user):
    get_user_if_user_exists = user_operations.get_user_by(already_registered_user.id)
    assert get_user_if_user_exists.id == already_registered_user.id


@pytest.mark.user_operations
def test_get_user_by_raises_exception(user_operations):
    with pytest.raises(exceptions.UserOperationsError):
        user_not_registered_username = "not_registered_username"
        _ = user_operations.get_user_by(user_not_registered_username)


@pytest.mark.user_operations
def test_reset_user_password(user_operations, already_registered_user):
    new_password = "testing_123"
    user_operations.reset_user_password(already_registered_user.id, new_password)
    get_user_if_user_exists = user_operations.get_user_by(already_registered_user.id)

    assert Users.verify_password(get_user_if_user_exists.hash_password, new_password)


@pytest.mark.user_operations
def test_reset_user_username(user_operations, already_registered_user):
    new_username = "testing_username"
    user_operations.reset_user_username(already_registered_user.id, new_username)
    get_user_if_user_exists = user_operations.get_user_by(already_registered_user.id)

    assert get_user_if_user_exists.username == new_username


@pytest.mark.user_operations
def test_reset_user_email(user_operations, already_registered_user):
    new_email = "testing@gmail.com"
    user_operations.reset_user_username(already_registered_user.id, new_email)
    get_user_if_user_exists = user_operations.get_user_by(already_registered_user.id)

    assert get_user_if_user_exists.username == new_email


@pytest.mark.user_operations
def test_get_username(user_operations, already_registered_user):
    found_username = user_operations.get_username(already_registered_user.id)

    assert already_registered_user.username == found_username


@pytest.mark.user_operations
def test_set_email_as_verified(user_operations, already_registered_user):
    user_operations.set_email_as_verified(already_registered_user.id)

    found_user = user_operations.get_user_by(already_registered_user.id)

    assert found_user.is_email_verified


@pytest.mark.user_operations
def test_check_if_email_is_verified_error(
    user_operations, already_registered_user_unverified
):
    with pytest.raises(exceptions.UserOperationsError):
        user_operations.check_if_email_is_verified(
            already_registered_user_unverified.id
        )


@pytest.mark.user_operations
def test_set_user_as_admin(
    user_operations, already_registered_admin, already_registered_user
):
    user_operations.set_user_as_admin(
        already_registered_admin.id, already_registered_user.username
    )
    user_found = user_operations.get_user_by(already_registered_user.id)
    assert user_found.is_admin == True
