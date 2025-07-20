#!/usr/bin/env python3
"""
This module defines a GithubOrgClient class that interacts with GitHub's API.
"""

from typing import List, Dict
from utils import get_json, memoize


class GithubOrgClient:
    """Client to fetch GitHub organization information."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize client with organization name."""
        self.org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Fetch organization information."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """Get the URL of public repositories from organization info."""
        return self.org.get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        """Fetch list of public repositories, optionally filter by license."""
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo.get("name") for repo in repos]
        return [repo.get("name") for repo in repos if self.has_license(repo, license)]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has a specific license."""
        license_info = repo.get("license")
        return license_info and license_info.get("key") == license_key

