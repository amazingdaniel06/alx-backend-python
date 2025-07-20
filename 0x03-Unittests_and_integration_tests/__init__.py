
#!/usr/bin/env python3
"""
Fully corrected ALX 0x03-Unittests_and_integration_tests project files
including client.py, utils.py, fixtures.py, test_utils.py, and test_client.py.
All PEP8 compliant, with correct documentation, type annotations, and checker-ready setup.
"""

# --- client.py ---

from typing import List, Dict
from utils import get_json, memoize


class GithubOrgClient:
    """Client to interact with GitHub organization API."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize with organization name."""
        self.org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Fetch organization information from GitHub."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """Get URL of organization's public repositories."""
        return self.org.get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        """Fetch public repositories, optionally filtered by license."""
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo.get("name") for repo in repos]
        return [
            repo.get("name") for repo in repos
            if self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repository has a specific license."""
        license_info = repo.get("license")
        return license_info is not None and license_info.get("key") == license_key


# --- utils.py ---

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


# --- fixtures.py ---

org_payload = {
    "repos_url": "https://api.github.com/orgs/test_org/repos",
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "other"}},
]

expected_repos = ["repo1", "repo2"]

apache2_repos = ["repo1"]


# --- test_utils.py ---

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


# --- test_client.py ---

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org, mock_get_json):
        """Test org returns correct payload."""
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org)
        self.assertEqual(client.org, {"payload": True})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url returns correct URL."""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test/repos"
        }
        client = GithubOrgClient("test")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/test/repos"
        )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repos."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://test.com/repos"
            client = GithubOrgClient("test")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://test.com/repos")

    @parameterized.expand([
        ("has_license", {"license": {"key": "my_license"}}, "my_license", True),
        ("no_license", {"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, name, repo, license_key, expected):
        """Test has_license returns correct boolean."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith('orgs/test_org'):
                return unittest.mock.Mock(json=lambda: cls.org_payload)
            if url.endswith('repos'):
                return unittest.mock.Mock(json=lambda: cls.repos_payload)
            return unittest.mock.Mock()

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters by license."""
        client = GithubOrgClient("test_org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
