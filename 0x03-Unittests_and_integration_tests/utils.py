#!/usr/bin/env python3
"""
Utilities module with JSON fetching and memoization.
"""

from typing import Mapping, Sequence, Any, Dict
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map by following path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    """Fetch JSON from a given URL."""
    response = requests.get(url)
    return response.json()


def memoize(method):
    """Decorator to cache method results."""
    attr_name = f"_memoized_{method.__name__}"

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
