#!/usr/bin/env python3
"""Unit tests for client module"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct value"""
        expected = {"payload": True}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL"""
        payload = {"repos_url": "http://example.com/org/repos"}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=property,
            return_value=payload
        ):
            client = GithubOrgClient("google")
            result = client._public_repos_url

        self.assertEqual(result, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns list of repo names"""
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=property,
            return_value="http://example.com/repos"
        ) as mock_url:

            client = GithubOrgClient("google")
            result = client.public_repos()

        self.assertEqual(result, ["repo1", "repo2"])
        mock_get_json.assert_called_once()
        mock_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()
