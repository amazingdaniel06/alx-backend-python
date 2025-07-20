#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns correct payload."""
        mock_get.return_value = Mock(json=lambda: test_payload)
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""

    def test_memoize(self):
        """Test memoize caches method result."""

        class TestClass:
            """Test class for memoization."""

            def a_method(self):
                """Simple method."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            test_obj = TestClass()
            self.assertEqual(test_obj.a_property(), 42)
            self.assertEqual(test_obj.a_property(), 42)
            mock_method.assert_called_once()
