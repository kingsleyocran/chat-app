"""Consumer

This module is demonstrates how the operations
for connecting, accepting, sending and receiving
websocket operations

Attributes:
    chat_consumer_logger (object): Logger
    AUTH_URL (str): Account service url
    resource (object): Resource definition for trace metrics
    jaeger_exporter (object): Jaeger Exportor for the trace metrics

"""
import asyncio
import json
from threading import Thread
from typing import Any, Union
from urllib.parse import parse_qs

import requests
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from websocket.tools.log import Log

from ..models import Message

resource = Resource(attributes={SERVICE_NAME: "chat.service"})

jaeger_exporter = JaegerExporter(
    agent_host_name=settings.JAEGER_HOST,
    agent_port=settings.JAEGER_PORT,
)

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer_provider().get_tracer(__name__)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)  # noqa


chat_consumer_logger = Log(__file__)
AUTH_URL = settings.AUTH_MANAGEMENT_URL
SUPPORT_URL = settings.SUPPORT_URL


class ChatConsumer(AsyncWebsocketConsumer):
    """Chat Consumer Process

    This class is responsible for performing
    connect, accept, sending and receiving
    messages or websocket. It also authenticates
    a user who wants to connect.
    """

    _room_group_name = "default_group"
    _room_name = "default_name"
    _user = ""

    async def fetch_messages(self, data):
        from_author = data["from_author"]
        to_author = data["to_author"]

        messages = await database_sync_to_async(
            Message.last_20_messages_from_author_to_author
        )(from_author=from_author, to_author=to_author)
        if len(messages) < 1:
            content = {
                "messages": [{"messages": None}],
                "from_author": from_author,
                "to_author": to_author,
            }
        else:
            content = {
                "messages": self.messages_to_json(messages),
                "from_author": from_author,
                "command": data.get("command"),
            }
        await self.send_chat_message(content)

    def messages_to_json(self, messages: list[Message]):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message: Message):
        return {
            "messages": message.message,
            "message_id": message.id,
            "created_at": str(message.created_at),
            "from_author": message.from_author,
            "to_author": message.to_author,
        }

    async def new_messages(self, data):
        from_author = data.get("from_author")
        to_author = data.get("to_author")
        messages = data.get("messages")

        created_message = await sync_to_async(Message.objects.create)(
            from_author=from_author, to_author=to_author, message=messages
        )
        content = {
            "messages": [self.message_to_json(created_message)],
            "from_author": from_author,
            "command": data.get("command"),
        }
        await self.send_chat_message(content)

    async def new_bot_message(self, issuer: str, message: str):
        from_author = "DaveAI"
        support_message = await self.get_reply(message)
        content = {
            "from_author": from_author,
            "to_author": issuer,
            "messages": support_message,
            "command": "new_message",
        }
        await self.new_messages(content)

    async def command_centre(self, data: dict[str, str]):
        """Command Centre

        This method is responsible for
        executing the commands
        """
        command = data.get("command")

        commands = {
            "fetch_messages": self.fetch_messages,
            "new_message": self.new_messages,
            "bot_message": self.new_bot_message,
        }

        await commands.get(command)(data)

    async def connect(self) -> None:
        """Connect

        This method is responsible for allowing
        connections to the websocket
        """
        if await self.is_user_authenticated():
            # accept the connection
            await self.accept()
            # extract the chat room name from route
            self._room_name = self.get_room_name()
            # create a group name
            self._room_group_name = f"chat_app_{self._room_name}"

            # add a channel layer to add a group name
            await self.channel_layer.group_add(
                self._room_group_name, self.channel_name  # type: ignore
            )
            # send a message to the group when they are connected
            await self.channel_layer.group_send(
                self._room_group_name,
                # message to send to group
                {
                    # function name to send message
                    "type": "connection_established",
                    "message": "You are now connected",
                },
            )

    async def connection_established(self, event: Any) -> None:
        """Connection established

        This connection is responsible for
        sending a success message when you are
        authenticated to the system

        Args:
            event (object): event raised by the socket
        """
        message = event.get("message")
        await self.send(
            text_data=json.dumps(
                {
                    "messages": message,
                    "username": str(self.scope.get("user")),
                    "type": "start",
                }
            )
        )

    async def chat_bot_message(self, event: Any) -> None:
        """Chat Bot Stream

        This method is responsible for
        sending message to a group channel
        for chat support

        Args:
            event (object): event raised by the socket
        """
        message = event.get("message")
        issuer = event.get("issuer")
        command = event.get("command")
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_bot_message",
                    "message": message,
                    "issuer": issuer,
                    "command": command,
                }
            )
        )

    def between_callback_for_bot(self, issuer, message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.new_bot_message(issuer, message))
        loop.close()

    async def chat_message(self, event: Any) -> None:
        """Chat Stream

        This method is responsible for
        sending message to a group channel

        Args:
            event (object): event raised by the socket
        """
        message = event.get("message")
        issuer = event.get("issuer")
        command = event.get("command")

        json_data = json.dumps(
            {
                "type": "chat_message",
                "message": message,
                "issuer": issuer,
                "command": command,
            }
        )

        await self.send(text_data=json_data)

    async def receive(self, text_data: str) -> None:
        """Receive

        This method is responsible for
        receiving messages from a group channel

        Args:
            text_data (str): data sent through the channel
        """
        text_data_json = json.loads(text_data)
        self._user = text_data_json.get("from_author")
        to_author = text_data_json.get("to_author")

        try:
            await self.command_centre(text_data_json)
            thread_for_bot = Thread(
                target=self.between_callback_for_bot,
                args=(
                    text_data_json.get("from_author"),  # noqa
                    text_data_json["messages"],
                ),
            )

            if to_author == "DaveAI":
                thread_for_bot.start()

        except Exception as e:
            print(e)

    async def send_chat_message(
        self,
        data: dict[str, Any],
        channel_type: str = "chat_message",
    ) -> None:
        message = data.get("messages")
        issuer = data.get("from_author")
        command = data.get("command")
        to_author = data.get("to_author")
        await self.channel_layer.group_send(
            self._room_group_name,
            {
                "type": channel_type,
                "message": message,
                "issuer": issuer,
                "command": command,
                "to_author": to_author,
            },
        )

    @tracer.start_as_current_span("support-request-time")
    async def get_reply(self, message: str) -> str:
        """Get Reply

        This method is responsible for
        getting a reply from a support
        system

        Args:
            message (str): message to be replied

        Returns:
            str: reply from the system
        """
        response = requests.post(
            f"{SUPPORT_URL}/api/v1/support", json={"question": message}
        )
        support_message = (
            response.json()["answer"]
            if response.status_code == 200
            else "Under Maintainance"
        )
        return support_message

    async def disconnect(self, close_code=None):
        """Disconnect from websocket

        This method is responsible for disconnecting
        a user from a socket

        Args:
            close_code

        Raises:
            AttributeError
        """
        try:
            # discard a group name
            await self.channel_layer.group_discard(
                self._room_group_name, self.channel_name
            )
        except AttributeError as exc:
            chat_consumer_logger.exception(exc.args[0])

    @tracer.start_as_current_span("auth-request-time")
    async def is_user_authenticated(self) -> Union[bool, None]:
        """User is authenticated

        This method is responsible for
        authenticating a user before joining
        a channel

        Returns:
            bool: True is successful, False otherwise
        """
        query_string = self.scope["query_string"].decode("utf-8")
        params = parse_qs(query_string)
        token_key = params.get("token")[0]
        headers = {
            "Authorization": f"Bearer {token_key}",
            "Content-type": "application/json",
        }
        response = requests.get(f"{AUTH_URL}/api/v1/username", headers=headers)
        if response.status_code == 200:
            self.scope["user"] = response.json()["message"]
            return True
        await self.disconnect()

    def get_room_name(self):
        """Get the room name

        Returns:
            str: the room name
        """
        route = self.scope.get("url_route")
        keywords = route.get("kwargs")
        room_name = keywords.get("room_name")
        return room_name
