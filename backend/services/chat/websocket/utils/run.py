"""Run utility

This module execute a process in async mode
"""
import asyncio


def async_return(result):
    """Run result in async mode
    Args:
        result (object): variable to run in async mode
    Returns:
        object : async variable
    """
    f = asyncio.Future()
    f.set_result(result)
    return f
