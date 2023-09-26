"""Application Builder and App Instance

This module is responsible for creating fastapi
application instances and configurating the
instance with the neccessary features

Attributes:
    settings (object): Application settings
"""
from typing import Union

import fastapi
from api.v1.router import support
from config import setting
from core import model
from error import exceptions
from fastapi.middleware.cors import CORSMiddleware
from handlers.exceptions import AppExceptionHandler
from interfaces import builder
from starlette_exporter import PrometheusMiddleware, handle_metrics

settings = setting.Settings()


class AppSingleton:
    """Application Instance creation

    This class instantiate an application
    only once.
    Attributes:
        _app_instance (object, None): Application instance

    """

    _app_instance = None

    @classmethod
    def get_app_instance(cls) -> Union[fastapi.FastAPI, None]:
        """Instantiate a fastapi application

        This method generates a fastapi application
        instance

        Returns:
            object: fastapi application instance
        """
        if cls._app_instance is None:
            cls._app_instance = fastapi.FastAPI()
        return cls._app_instance


class AppBuilder(builder.AppBuilderInterface):
    """Application Builder class

    This class builds adds features to a new or
    existing fastapi application instance

    Attributes:
        _app (object): The fastapi application

    """

    def __init__(self) -> None:
        """Construct a new application"""
        self._app = AppSingleton.get_app_instance()

    def register_exceptions(self) -> None:
        """Register all exceptions to be used

        This method is used to handle all
        exceptions for the application
        """
        self._app.add_exception_handler(
            exceptions.ModelError, AppExceptionHandler.operations
        )

    def register_middlewares(self) -> None:
        """Register all middlewares

        This method is used to handle all
        middlewares for the application
        """
        self._app.add_middleware(
            PrometheusMiddleware,
            app_name=settings.APP_TITLE,
            prefix="support_service",
            group_paths=True,
            buckets=[
                0.01,
                0.025,
                0.05,
                0.075,
                0.1,
                0.25,
                0.5,
                0.75,
                1.0,
                2.5,
                5.0,
                7.5,
                10.0,
            ],
        )
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def register_routes(
        self,
    ) -> Union[None, fastapi.responses.RedirectResponse]:  # type: ignore
        """Register routes to be used

        This method is used to handle all
        routers for the application
        """

        self._app.include_router(
            support.router, prefix=settings.API_PREFIX, tags=["Support"]
        )
        self._app.add_route("/metrics", handle_metrics)

        @self._app.get("/", include_in_schema=False)
        def index() -> fastapi.responses.RedirectResponse:
            """Redirect visitor to the docs page

            Returns:
                object: redirect response
            """
            return fastapi.responses.RedirectResponse("/docs")

        return index()

    def load_application_model(self) -> None:
        """Load the AI model on Start of the application"""

        @self._app.on_event("startup")
        def load_model() -> None:
            """Load the AI model"""
            model.DaveModel()

        return load_model()

    def add_app_details(
        self, title: str = None, description: str = None  # type: ignore
    ) -> None:
        """Append features to the fastapi instance

        This method is responsible for including
        details to the fastapi instance

        Args:
            title (str): Title used for the application
            description (str): Description for the application
        """
        self._app.title = title
        self._app.description = description

    def build_app(self) -> fastapi.FastAPI:
        """Build Application

        This method is used to construct the
        application

        Returns:
            object: fastapi instance
        """
        self.register_middlewares()
        self.register_exceptions()
        self.add_app_details(
            title=settings.APP_TITLE,
            description=settings.APP_DESCRIPTION,
        )
        self.load_application_model()
        self.register_routes()
        return self._app
