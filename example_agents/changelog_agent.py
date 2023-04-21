import os
from pydantic import BaseModel, validator
from agent_runner.agent import Agent
from typing import List, Dict
from dotenv import load_dotenv
from example_tools.github_commits.github_commits import GithubRecentCommits

load_dotenv()


class ChangelogAgent(Agent):
    class Input(BaseModel):
        input: List[str]

    class Output(BaseModel):
        commit_messages: Dict[str, List[str]]

    def run(self, input: Input) -> Output:
        github_token = os.environ["GITHUB_TOKEN"]
        github_recent_commits_tool = GithubRecentCommits()
        github_recent_commits_tool.github_token = github_token
        all_repo_commit_messages = {}

        for repo_url in input.input:
            repo_commit_messages = github_recent_commits_tool(repo_url)
            all_repo_commit_messages[repo_url] = repo_commit_messages

        return self.Output(commit_messages=all_repo_commit_messages)
