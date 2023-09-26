"""URl module

This module defines the url route for testing
the websocket functionality
"""
from django.urls import path

from . import views

urlpatterns = [path("<str:room_name>", views.index, name="index")]
