from classes.console import Console
from classes.github.client import Auth, Client
from classes.matcher import Matcher
from classes.option.option_interface import OptionInterface
from classes.yaml_parser import YamlParser
from model.match import Match
from model.package_collection import Collection
from typing import Any, List


class AbstractOption(OptionInterface):

    def __init__(self, console: Console, yaml_parser: YamlParser):
        super().__init__(console, yaml_parser)
        self.console: Console = console
        self.args: Any = console.get_args()
        self.yaml_parser: YamlParser = yaml_parser

    @staticmethod
    def get_matches(config: str, json: bool = False) -> List[Match]:
        return Matcher.get_json_matches(config) if json else Matcher.get_lock_matches(config)

    @staticmethod
    def get_not_equal(matches: List[Match], fields: List[str]) -> List[Match]:
        filtered: List[Match] = []
        for match in matches:
            if not match.is_equal(fields):
                filtered.append(match)
        return filtered

    def get_package_names(self) -> List[str]:
        packages: Collection = self.yaml_parser.get_packages()
        package_names: List[str] = []
        for package in packages:
            package_names.append(package.name)
        return package_names

    def get_client(self) -> Client:
        auth: Auth = Auth()
        auth.parse_yaml(self.yaml_parser)
        return Client(auth)
