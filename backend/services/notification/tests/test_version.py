"""Test
"""
from consumers import __version__


def test_version() -> None:
    """Testing version number"""
    __version__ == "0.1.0"
