import os
from pydantic import BaseModel
from agent_runner.agent import Agent
from typing import List, Dict
from dotenv import load_dotenv
from example_tools.commit_summarizer.summarize_commits import (
    SummarizeCommits,
    SummarizeCommitsInput,
)
from example_tools.github_commits.github_commits import GithubRecentCommits

load_dotenv()


class ChangeLogInput(BaseModel):
    app_description: str
    repo_descriptions: str
    repo_list: List[str]


class ChangelogAgent(Agent):
    class Input(BaseModel):
        input: ChangeLogInput

    class Output(BaseModel):
        commit_messages: Dict[str, List[str]]

    def run(self, input: Input) -> Output:
        github_token = os.environ["GITHUB_TOKEN"]
        github_recent_commits_tool = GithubRecentCommits()
        github_recent_commits_tool.github_token = github_token
        all_repo_commit_messages = {}

        for repo_url in input.input.repo_list:
            repo_commit_messages = github_recent_commits_tool(repo_url)
            all_repo_commit_messages[repo_url] = repo_commit_messages

        summarize_commits = SummarizeCommits()

        query = {
            "commits_string": str(all_repo_commit_messages),
            "app_description": input.input.app_description,
            "repo_descriptions": input.input.repo_descriptions,
        }

        return summarize_commits(query)
