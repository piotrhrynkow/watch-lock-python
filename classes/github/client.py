from classes.yaml_parser import YamlParser
from github import Branch, Commit, Github, Repository
from typing import Dict, Optional


class Auth:

    def __init__(self, yaml_parser: YamlParser):
        self.login: Optional[str] = None
        self.password: Optional[str] = None
        self.token: Optional[str] = None
        if yaml_parser.get_token():
            self.token = yaml_parser.get_token()
        if yaml_parser.get_login() and yaml_parser.get_password():
            self.login = yaml_parser.get_login()
            self.password = yaml_parser.get_password()

    def get_props(self) -> Dict[str, str]:
        props: Dict[str, str] = {}
        if self.login and self.password:
            props["login_or_token"] = self.login
            props["password"] = self.password
        elif self.token:
            props["login_or_token"] = self.token
        return props


class Config:

    def __init__(self, yaml_parser: YamlParser):
        self.auth: Auth = Auth(yaml_parser)
        self.url: Optional[str] = None
        if yaml_parser.get_url():
            self.url = yaml_parser.get_url()

    def get_props(self) -> Dict[str, str]:
        props: Dict[str, str] = self.auth.get_props()
        if self.url:
            props["base_url"] = self.url
        return props


class Client:

    def __init__(self, auth: Auth):
        self.github: Github = Github(**auth.get_props())

    def get_client(self) -> Github:
        return self.github

    def get_last_sha(self, repository: str, branch: str = "master") -> str:
        repo: Repository = self.github.get_repo(repository)
        branch: Branch = repo.get_branch(branch)
        commit: Commit = branch.commit
        return commit.sha
