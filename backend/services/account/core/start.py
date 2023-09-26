"""Initialize application entry

This module is responsible for initializing
an application to be used by the main module
"""
import fastapi

from core.build import AppBuilder
from interfaces import factory


class AppFactory(factory.AppFactoryInterface):
    """Application factory to generate
    fully bundled fastapi application

    Returns:
        object: fastapi instance
    """

    @staticmethod
    def initialize_app() -> fastapi.FastAPI:
        app_instance = AppBuilder()
        return app_instance.build_app()
