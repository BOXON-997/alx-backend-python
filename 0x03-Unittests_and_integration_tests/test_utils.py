#!/usr/bin/env python3
"""Unit tests for utils functions"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_msg}'")


class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Ensure get_json calls requests.get and returns response.json()"""

        # Prepare mock response
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch where `requests` is looked up inside utils (important)
        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)

            # assert requests.get was called once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # assert get_json returned the payload from response.json()
            self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
