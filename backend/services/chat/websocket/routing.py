"""Routing for Websocket

This module defines the routing definition
"""
from django.urls import re_path

from .controller import consumer

websocket_patterns = [
    re_path(
        r"ws/chat/(?P<room_name>\w+)/$",
        consumer.ChatConsumer.as_asgi(),
        name="websocker_url",
    )
]
