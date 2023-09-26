"""Configuration for test

This module shows the configuration
done before you run a test

"""
import pytest
from channels.testing import WebsocketCommunicator
from websocket.controller import consumer


@pytest.fixture
@pytest.mark.asyncio
async def websocket_instance():
    test_token = "ghana"
    communicator = WebsocketCommunicator(
        consumer.ChatConsumer.as_asgi(), f"/ws/chat/ghana/?token={test_token}"
    )
    return communicator
