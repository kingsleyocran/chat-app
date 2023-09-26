"""Interfaces for Parsers
"""

from abc import ABC, abstractclassmethod


class ParserInterface(ABC):
    """Parser Interface

    Describe the structure for every instance
    of parser
    """

    @abstractclassmethod
    def get(cls):
        """Implement A Get method"""
