#!/usr/bin/env python3
from typing import Any, Mapping, Sequence, Callable
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested map with a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Any:
    """GET request and return JSON content."""
    response = requests.get(url)
    return response.json()


def memoize(method: Callable) -> Callable:
    """Decorator to cache method output."""
    attr_name = "_memoized_" + method.__name__

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
