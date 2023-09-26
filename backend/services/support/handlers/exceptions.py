"""Exception handlers

This module demonstrates how to handle any
Exception that occurs within the application

Attributes:
    logger (object): A log utility for logging
"""
import fastapi

from error import exceptions
from utils.log import Log

logger = Log(__file__)


class AppExceptionHandler:
    """Application Exception Handler"""

    @staticmethod
    def operations(
        request: fastapi.Request,
        exec: exceptions.ModelError,  # type: ignore
    ):
        """Operations exception handler

        This method is responsible for handling
        any operation exceptions raised

        Args:
            request (object): request from the client
            exec (object): Exception raised

        Returns:
            object: Fastapi Json response
        """
        logger.error(exec.msg)
        return fastapi.responses.JSONResponse(
            # type: ignore
            content={"error": exec.msg},
            status_code=exec.status_code,
        )
