#!/usr/bin/env python3
"""
This module provides utility functions for accessing nested maps,
retrieving JSON from URLs, and memoization functionality.
"""

from typing import Any, Mapping, Sequence, Callable
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested object in nested_map with a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Any:
    """Retrieve JSON content from a given URL."""
    response = requests.get(url)
    return response.json()


def memoize(method: Callable) -> Callable:
    """Decorator to cache the result of method calls."""
    attr_name = "_memoized_" + method.__name__

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper

