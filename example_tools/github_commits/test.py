from github_commits import GithubRecentCommits

github_token = ""
repo_url = "https://github.com/hwchase17/langchain"
github_recent_commits_tool = GithubRecentCommits()
github_recent_commits_tool.github_token = github_token
commit_messages = github_recent_commits_tool(repo_url)
print(commit_messages)
