# resources.py
"""
Resource functions for the MCP server.
This module contains resource functions that can be used by the MCP server.
"""

def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

def get_farewell(name: str) -> str:
    """Get a personalized farewell"""
    return f"Goodbye, {name}! See you later!"