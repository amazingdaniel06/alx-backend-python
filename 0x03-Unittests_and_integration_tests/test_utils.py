#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""

    @parameterized.expand([
        ("simple", {"a": 1}, ("a",), 1),
        ("nested", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing", {}, ("a",), 'a'),
        ("key_error", {"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path, missing_key):
        """Test KeyError is raised when key is missing."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{missing_key}'")


class TestGetJson(unittest.TestCase):
    """Tests for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url, payload, mock_get):
        """Test get_json returns expected payload."""
        mock_get.return_value.json.return_value = payload
        self.assertEqual(get_json(url), payload)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""

    def test_memoize(self):
        """Test memoize caches method calls."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            self.assertEqual(obj.a_property(), 42)
            self.assertEqual(obj.a_property(), 42)
            mock_method.assert_called_once()
