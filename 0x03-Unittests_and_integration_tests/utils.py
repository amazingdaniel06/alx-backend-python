#!/usr/bin/env python3
"""
Utility functions for nested map access, JSON fetching, and memoization.
"""

from typing import Mapping, Any, Sequence, Dict
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a nested object in nested_map with a sequence of keys.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    """
    Get JSON from the provided URL.
    """
    response = requests.get(url)
    return response.json()


def memoize(method):
    """
    Decorator to cache method output.
    """
    attr_name = f"_{method.__name__}"

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
