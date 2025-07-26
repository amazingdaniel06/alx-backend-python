#!/usr/bin/env python3
"""
Client module for interacting with GitHub organization data.
"""

from typing import List, Dict, Optional
from utils import get_json, memoize


class GithubOrgClient:
    """
    GithubOrgClient class to interact with GitHub API.
    """

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize client with organization name."""
        self.org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Fetch organization information."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
  @property
def org(self):
    """
    Retrieve organization information from the GitHub API.

    Returns:
        dict: A dictionary containing details about the organization.
    """
    return get_json(f"https://api.github.com/orgs/{self.org_name}")

    def public_repos(self, license: Optional[str] = None) -> List[str]:
        """
        Get list of public repositories. Optionally filter by license.
        """
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo.get("name") for repo in repos]
        return [
            repo.get("name")
            for repo in repos
            if self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if a repository has a specific license."""
        license_info = repo.get("license")
        return bool(license_info and license_info.get("key") == license_key)
