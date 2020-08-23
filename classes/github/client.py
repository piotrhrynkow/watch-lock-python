from classes.yaml_parser import YamlParser
from github import Branch, Commit, Github, Repository
from typing import List, Optional


class Auth:

    def __init__(self):
        self.login: Optional[str] = None
        self.password: Optional[str] = None
        self.token: Optional[str] = None

    def parse_yaml(self, yaml: YamlParser):
        if yaml.get_token():
            self.token = yaml.get_token()
        if yaml.get_login() and yaml.get_password():
            self.login = yaml.get_login()
            self.password = yaml.get_password()

    def set_token(self, token: str):
        self.token = token

    def set_login(self, login: str, password: str):
        self.login = login
        self.password = password

    def get_props(self) -> List[str]:
        return [self.token] if self.token is not None else [self.login, self.password]


class Client:

    def __init__(self, auth: Auth):
        self.github: Github = Github(*auth.get_props())

    def get_client(self) -> Github:
        return self.github

    def get_last_sha(self, repository: str, branch: str = "master") -> str:
        repo: Repository = self.github.get_repo(repository)
        branch: Branch = repo.get_branch(branch)
        commit: Commit = branch.commit
        return commit.sha
