#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient class.

This module tests the GithubOrgClient class defined in client.py.
It includes:
- Unit tests for methods and properties
- Integration tests simulating GitHub API responses
- Parameterized and mocked testing strategies

Each test ensures that API calls, responses, and filtering logic
in GithubOrgClient work as expected.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


# Fixtures embedded directly
ORG_PAYLOAD = {
    "login": "testorg",
    "repos_url": "https://api.github.com/orgs/testorg/repos"
}
REPOS_PAYLOAD = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "other-license"}},
]
EXPECTED_REPOS = ["repo1", "repo2"]
APACHE2_REPOS = ["repo1"]


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct payload"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test _public_repos_url returns repos_url from org"""
        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = ORG_PAYLOAD

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, ORG_PAYLOAD["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct list of repo names"""
        mock_get_json.return_value = REPOS_PAYLOAD

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = ORG_PAYLOAD["repos_url"]

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, EXPECTED_REPOS)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license correctly evaluates license match"""
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


class MockResponse:
    """Mocked response for requests.get().json()"""
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


@parameterized_class([
    {
        "org_payload": ORG_PAYLOAD,
        "repos_payload": REPOS_PAYLOAD,
        "expected_repos": EXPECTED_REPOS,
        "apache2_repos": APACHE2_REPOS,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with patching only for HTTP requests"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get with fixture responses"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/testorg":
                return MockResponse(cls.org_payload)
            if url == cls.org_payload.get("repos_url"):
                return MockResponse(cls.repos_payload)
            return None

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repo names"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns only repos with license"""
        client = GithubOrgClient("testorg")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()
