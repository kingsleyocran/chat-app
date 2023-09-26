import pytest
import tests.test_data as test_data
from fastapi_jwt_auth.exceptions import RevokedTokenError


@pytest.mark.route_account
def test_login_route(client, already_created_account):
    login_response = client.post("/login", json=test_data.test_login_data)
    assert login_response.status_code == 200


@pytest.mark.route_account
def test_refresh_route(client, already_logged_in_response):
    headers = {
        "Authorization": f"Bearer {already_logged_in_response.json()['refresh_token']}"
    }
    refresh_response = client.post(
        "/refresh",
        json=test_data.test_login_data,
        headers=headers,
    )
    assert refresh_response.status_code == 200


@pytest.mark.route_account
def test_logout_route(client, already_logged_in_response):
    headers = {
        "Authorization": f"Bearer {already_logged_in_response.json()['access_token']}"
    }
    logout_response = client.post(
        "/logout",
        json=test_data.test_login_data,
        headers=headers,
    )
    assert logout_response.status_code == 200


@pytest.mark.route_account
def test_access_route_after_logout(client, already_logged_in_response):
    headers = {
        "Authorization": f"Bearer {already_logged_in_response.json()['access_token']}"
    }
    logout_response = client.post(
        "/logout",
        json=test_data.test_login_data,
        headers=headers,
    )
    assert logout_response.status_code == 200

    headers_1 = {
        "Authorization": f"Bearer {already_logged_in_response.json()['access_token']}"
    }
    with pytest.raises(RevokedTokenError):
        client.get(
            "/username",
            headers=headers_1,
        )
