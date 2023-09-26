import pytest

from tests import test_data


@pytest.mark.route_users
@pytest.mark.parametrize(
    "expected_json", [({"username": "test_user", "email": "test_email@test.com"})]
)
def test_register_route(client, expected_json):
    response = client.post("/register", json=test_data.test_user_data)
    assert response.json() == expected_json
    assert response.status_code == 200


@pytest.mark.route_users
def test_change_email_route(client, already_logged_in_response):
    new_email = "test1@email.com"

    headers = {
        "Authorization": f"Bearer {already_logged_in_response.json()['access_token']}"
    }
    # change email
    change_email_response = client.post(
        "/change/email", headers=headers, json={"email": new_email}
    )
    assert change_email_response.status_code == 200
    assert change_email_response.json() == {"message": "email changed successfully"}


@pytest.mark.route_users
def test_change_username_route(client, already_logged_in_response):
    new_username = "test_new_username"

    headers = {
        "Authorization": f"Bearer {already_logged_in_response.json()['access_token']}"
    }
    # change username
    change_username_response = client.post(
        "/change/username", headers=headers, json={"username": new_username}
    )
    assert change_username_response.status_code == 200
    assert change_username_response.json() == {
        "message": "username changed successfully"
    }


@pytest.mark.route_users
def test_change_password_route(client, already_logged_in_response):
    new_password = "test_user_password"
    headers = {
        "Authorization": f"Bearer {already_logged_in_response.json()['access_token']}"
    }
    # get password
    change_password_response = client.post(
        "/change/password",
        headers=headers,
    )

    assert change_password_response.status_code == 200

    # change password
    headers_2 = {
        "Authorization": f"Bearer {change_password_response.json()['access_token']}"
    }

    change_password_confirm_response = client.post(
        "/change/password/confirm", headers=headers_2, json={"password": new_password}
    )

    assert change_password_confirm_response.status_code == 200
    assert change_password_confirm_response.json() == {
        "message": "changed password successfully"
    }


@pytest.mark.route_users
def test_admin_route(
    client, already_logged_in_admin_response, already_logged_in_response
):
    headers = {
        "Authorization": (
            f"Bearer {already_logged_in_admin_response.json()['access_token']}"
        )
    }

    add_admin_response = client.post(
        "/admin",
        json={"username": "test_user"},
        headers=headers,
    )
    assert add_admin_response.status_code == 200
