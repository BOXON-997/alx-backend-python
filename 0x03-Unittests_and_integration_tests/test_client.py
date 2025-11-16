#!/usr/bin/env python3
"""Unit tests for client module"""
from parameterized import parameterized, parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

from client import GithubOrgClient

import unittest
from unittest.mock import patch
from unittest.mock import patch, Mock


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

    @parameterized.expand([
    ({"license": {"key": "my_license"}}, "my_license", True),
    ({"license": {"key": "other_license"}}, "my_license", False),
    ])

    def test_has_license(self, repo, license_key, expected):
        """Test the has_license method returns correct bool"""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get with custom side effects"""

        def side_effect(url):
            if url.endswith("google"):
                return Mock(json=lambda: cls.org_payload)
            if url.endswith("repos"):
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: None)

        cls.get_patcher = patch("requests.get", side_effect=side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop patcher for requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns only repos with APACHE2 license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
