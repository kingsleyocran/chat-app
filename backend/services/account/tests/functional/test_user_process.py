import pytest


@pytest.mark.workflow
@pytest.mark.parametrize(
    "workflow_user,expected_json",
    [
        (
            {
                "username": "workflow_user",
                "email": "workflow@test.com",
                "password": "workflow_password",
            },
            {"username": "workflow_user", "email": "workflow@test.com"},
        )
    ],
)
def test_user_workflow_process(client, user_operations, workflow_user, expected_json):
    # user first registers in the system
    response = client.post("/register", json=workflow_user)
    assert response.json() == expected_json
    assert response.status_code == 200

    # user verifies email
    user_found = user_operations.get_user_by("workflow_user")
    user_operations.set_email_as_verified(user_found.id)

    # user logs in into the system
    # with his credentials
    test_login_credientials = {
        "username": "workflow_user",
        "password": "workflow_password",
    }
    login_response = client.post("/login", json=test_login_credientials)
    assert login_response.status_code == 200

    # user can see his username
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    username_response = client.get("/username", headers=headers)
    assert username_response.status_code == 200

    # user can change usename if
    # not good
    # say new_username is foobar
    new_username = "foobar"
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    change_username_response = client.post(
        "/change/username", json={"username": new_username}, headers=headers
    )

    assert change_username_response.status_code == 200

    # user can also change email
    # new email is youlikeitright@yes.com
    new_email = "youlikeitright@yes.com"
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    change_email_response = client.post(
        "/change/email", json={"email": new_email}, headers=headers
    )

    assert change_email_response.status_code == 200

    # user can also change password
    # new password is youcantguessmypassword'
    new_password = "youcantguessmypassword"

    # first user request for password change
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    change_password_response = client.post("/change/password", headers=headers)

    assert change_password_response.status_code == 200

    # user confirms password change request
    headers = {
        "Authorization": f"Bearer {change_password_response.json()['access_token']}"
    }
    change_password_confirm_response = client.post(
        "/change/password/confirm",
        json={
            "password": new_password,
        },
        headers=headers,
    )

    assert change_password_confirm_response.status_code == 200

    # user decides to logout from the system
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    logout_response = client.post("/logout", headers=headers)

    assert logout_response.status_code == 200
