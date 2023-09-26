import pytest

from error import exceptions


@pytest.mark.account_operations
def test_create_account(account_operations, already_registered_user):
    account_operations.create_account(already_registered_user.id)
    account = account_operations.get_account_with_user_id(already_registered_user.id)

    assert account.user_id == already_registered_user.id

    # user string representation
    assert str(account) == f"{account.id}-{account.user.username}"


@pytest.mark.account_operations
def test_get_account_with_user_id_raises_exception(account_operations):
    with pytest.raises(exceptions.AccountOperationsError):
        fake_user_id = 100
        account_operations.get_account_with_user_id(fake_user_id)


@pytest.mark.account_operations
def test_set_account_as_active(
    account_operations, already_created_account, already_registered_user
):
    account_operations.set_account_as_active(already_registered_user.id)
    assert already_created_account.is_active


@pytest.mark.account_operations
def test_set_account_as_active(
    account_operations, already_created_account, already_registered_user
):
    account_operations.set_account_as_inactive(already_registered_user.id)
    assert not already_created_account.is_active


@pytest.mark.account_operations
def test_set_account_profile_pic(
    account_operations, already_created_account, already_registered_user
):
    profile_pic = "test.png"
    account_operations.set_account_profile_pic(already_registered_user.id, profile_pic)
    assert already_created_account.profile_pic == profile_pic


@pytest.mark.account_operations
def test_is_user_account_active(
    account_operations, already_created_account, already_registered_user
):
    account_state = account_operations.is_user_account_active(
        already_registered_user.id
    )
    assert already_created_account.is_active == account_state
