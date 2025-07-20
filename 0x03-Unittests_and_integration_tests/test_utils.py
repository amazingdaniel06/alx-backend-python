#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ("simple_access", {"a": 1}, ("a",), 1),
        ("nested_access", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep_nested_access", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test that access_nested_map returns expected value."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ("empty_map", {}, ("a",)),
        ("missing_key", {"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path):
        """Test access_nested_map raises KeyError for invalid path."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""

    @parameterized.expand([
        ("example_com", "http://example.com", {"payload": True}),
        ("holberton_io", "http://holberton.io", {"payload": False}),
    ])
    @patch('0x03-Unittests_and_integration_tests.utils.requests.get')
    def test_get_json(self, name, url, payload, mock_get):
        """Test that get_json returns expected JSON response."""
        mock_get.return_value = Mock(json=Mock(return_value=payload))
        result = get_json(url)
        self.assertEqual(result, payload)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches method output after first call."""

        class TestClass:
            """Inner test class with method to be memoized."""

            def a_method(self):
                """Simple method returning constant value."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property method."""
                return self.a_method()

        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:
            obj = TestClass()
            first_call = obj.a_property()
            second_call = obj.a_property()

            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)
            mock_method.assert_called_once()
