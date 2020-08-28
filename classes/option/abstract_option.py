from classes.console.console import Console
from classes.github.client import Auth, Client
from classes.package_matcher.package_matcher import PackageMatcher
from classes.option.option_interface import OptionInterface
from classes.yaml_parser import YamlParser
from classes.package_matcher.match import Match
from classes.model.package import Package
from typing import Any, List, Iterator


class AbstractOption(OptionInterface):

    def __init__(self, console: Console, yaml_parser: YamlParser):
        super().__init__(console, yaml_parser)
        self.console: Console = console
        self.args: Any = console.get_args()
        self.yaml_parser: YamlParser = yaml_parser

    @staticmethod
    def get_matches(config: str, json: bool = False) -> List[Match]:
        return PackageMatcher.get_json_matches(config) if json else PackageMatcher.get_lock_matches(config)

    def get_package_names(self) -> Iterator[str]:
        packages: List[Package] = self.yaml_parser.get_packages()
        return map(lambda package: package.name, packages)

    def get_client(self) -> Client:
        auth: Auth = Auth(self.yaml_parser)
        return Client(auth)
