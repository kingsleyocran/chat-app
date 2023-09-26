"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("websocket.urls")),
    path("", include("django_prometheus.urls")),
    path("search/", include("search.urls")),  # noqa
]
