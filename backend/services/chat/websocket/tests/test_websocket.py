"""Test Websocket

This module demonstrate the operations to test
websocket connection
"""
from unittest.mock import Mock, patch

import pytest

from ..utils.run import async_return

CUSTOMER_MODULE_LOC = "websocket.controller.consumer.ChatConsumer"

TEST_MESSAGE = "hello there"
PATCH_GET_REQUEST_PATH = "websocket.controller.consumer.requests.get"


@pytest.mark.asyncio
async def test_websocket_connect(websocket_instance):
    """Test websocket connection

    This function test the websocket connection
    """
    websocket = await websocket_instance
    with patch(
        f"{CUSTOMER_MODULE_LOC}.is_user_authenticated",
        return_value=async_return(True),
    ):
        connected, _ = await websocket.connect()
        assert connected


@pytest.mark.asyncio
async def test_websocket_connection_message(websocket_instance):
    """Test websocket connection message

    This function test the websocket success
    connection message
    """
    websocket = await websocket_instance

    with patch(
        f"{CUSTOMER_MODULE_LOC}.get_room_name",
        return_value="test_group_name",
    ):
        with patch(
            f"{CUSTOMER_MODULE_LOC}.is_user_authenticated",
            return_value=async_return(True),
        ):
            _, _ = await websocket.connect()
            response = await websocket.receive_json_from()
            assert response.get("type") == "start"
            assert response.get("messages") == "You are now connected"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_send_new_message(websocket_instance):
    """Test Send new messages"""
    websocket = await websocket_instance

    with patch(PATCH_GET_REQUEST_PATH) as mock_request:
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"message": "test_user"}
        mock_response.status_code = 200
        with patch(f"{CUSTOMER_MODULE_LOC}.get_room_name", return_value="ghana"):
            _, _ = await websocket.connect()
            # skip connection message
            _ = await websocket.receive_json_from()
            await websocket.send_json_to(
                {
                    "messages": TEST_MESSAGE,
                    "from_author": "test_user_sender",
                    "to_author": "test_user_receiver",
                    "command": "new_message",
                }
            )
            response = await websocket.receive_json_from()
            assert response.get("type") == "chat_message"
            assert response.get("issuer") == "test_user_sender"
            assert len(response.get("message")) == 1
            assert response.get("message")[0].get("messages") == TEST_MESSAGE
            assert response.get("message")[0].get("from_author") == "test_user_sender"
            assert response.get("command") == "new_message"

            await websocket.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_send_fetch_message(websocket_instance):
    """Test Send Fetch message request to websocket"""
    websocket = await websocket_instance

    with patch(PATCH_GET_REQUEST_PATH) as mock_request:
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"message": "test_user"}
        mock_response.status_code = 200
        with patch(f"{CUSTOMER_MODULE_LOC}.get_room_name", return_value="ghana"):
            _, _ = await websocket.connect()
            # skip connection message
            _ = await websocket.receive_json_from()
            await websocket.send_json_to(
                {
                    "from_author": "test_user_sender",
                    "to_author": "test_user_receiver",
                    "command": "fetch_messages",
                }
            )
            response = await websocket.receive_json_from()
            assert response.get("type") == "chat_message"
            assert response.get("issuer") == "test_user_sender"
            assert len(response.get("message")) == 1
            assert response.get("message")[0].get("messages") == TEST_MESSAGE
            assert response.get("message")[0].get("from_author") == "test_user_sender"
            assert response.get("message")[0].get("to_author") == "test_user_receiver"
            assert response.get("command") == "fetch_messages"

            await websocket.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_support_route(websocket_instance):
    """Test Chat Functionality with Support AI

    This function is used to test the interaction
    of the ai model
    """
    websocket = await websocket_instance

    with patch(PATCH_GET_REQUEST_PATH) as mock_request:
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"message": "test_user"}
        mock_response.status_code = 200
        with patch(f"{CUSTOMER_MODULE_LOC}.get_room_name", return_value="support"):
            _, _ = await websocket.connect()
            # skip connection message
            _ = await websocket.receive_json_from()

            with patch("websocket.controller.consumer.requests.post") as m_post:
                mock_response = Mock()
                m_post.return_value = mock_response
                mock_response.status_code = 200
                mock_response.json.return_value = {"answer": "Hey, what's up"}
                await websocket.send_json_to(
                    {
                        "from_author": "test_user_sender",
                        "to_author": "DaveAI",
                        "messages": "Hey",
                        "command": "new_message",
                    }
                )
                response = await websocket.receive_json_from()
                assert response.get("type") == "chat_message"
                assert response.get("issuer") == "test_user_sender"
                assert len(response.get("message")) == 1
                assert response.get("message")[0].get("messages") == "Hey"
                assert (
                    response.get("message")[0].get("from_author") == "test_user_sender"
                )
                assert response.get("message")[0].get("to_author") == "DaveAI"
                assert response.get("command") == "new_message"

                await websocket.disconnect()


@pytest.mark.asyncio
async def test_websocket_disconnect(websocket_instance):
    websocket = await websocket_instance
    await websocket.disconnect()
    assert await websocket.receive_nothing()
