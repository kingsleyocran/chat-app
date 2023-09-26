from django.http import JsonResponse

"""Websocket View

This module the endpoint view for websocket
"""


"""
# uncomment this to test websocket out
from django.shortcuts import render
def index(request, room_name):
    return render(request, "index.html", {"room_name": room_name})
"""


def index(request, room_name):
    """Index View

    Args:
        request (object): request
        room_name (str): room name to join

    Returns:
        object : Json response
    """
    return JsonResponse(data={"message": "This API is used for streaming"})
