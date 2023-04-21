import requests
import re
from datetime import datetime, timedelta
from typing import List
from langchain.tools import BaseTool


class GithubRecentCommits(BaseTool):
    github_token = ""
    name = "GithubRecentCommits"
    description = "use this to query for recent commits to a GitHub repo"

    def _validate_github_url(self, url: str) -> bool:
        pattern = r"https://github\.com/[\w.-]+/[\w.-]+/?"
        return bool(re.match(pattern, url))

    def _run(self, repo_url: str) -> List[str]:
        """Retrieves all commit messages for commits made in the last 2 weeks."""

        if not self._validate_github_url(repo_url):
            raise ValueError("Invalid GitHub repository URL")

        # Extract the owner and repo name from the URL
        owner, repo_name = repo_url.rstrip("/").split("/")[-2:]

        # Calculate the timestamp for 2 weeks ago
        two_weeks_ago = (datetime.now() - timedelta(weeks=2)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        # Prepare the API URL
        api_url = f"https://api.github.com/repos/{owner}/{repo_name}/commits?since={two_weeks_ago}"
        headers = {}

        # Prepare the headers with the personal access token
        if self.github_token != "":
            headers = {"Authorization": f"Bearer {self.github_token}"}

        # Send the request to the GitHub API
        response = requests.get(api_url, headers=headers)
        commits = response.json()

        if type(commits) is dict:
            raise Exception(commits["message"])

        # Extract commit messages from the response
        commit_messages = [commit["commit"]["message"] for commit in commits]

        return commit_messages

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GithubRecentCommits does not support async")
