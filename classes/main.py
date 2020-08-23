from classes.console import Console
from classes.github.client import Auth, Client
from classes.lock_modifier.lock_modifier import LockModifier
from classes.lock_modifier.result import Result
from classes.matcher import Matcher
from classes.table import Table
from classes.yaml_parser import YamlParser
from classes.yaml_replacer import YamlReplacer
from model.match import Match
from model.package import Package
from model.package_collection import Collection
import sys
from typing import Any, List


class Main:

    def __init__(self):
        console = Console()
        args: Any = console.get_args()
        self.yaml_parser: YamlParser = YamlParser(args.config)

        if Console.TYPE_SEARCH == console.get_type():
            table: Table = Table(["Directory", "Name", "Reference expected", "Reference actual"])
            value_type: List[str] = ["source", "reference"]
            matches: List[Match] = self.get_matches(args.config)
            if not args.all:
                matches: List[Match] = self.get_not_equal(matches, value_type)
            for match in matches:
                is_equal: bool = match.is_equal(value_type)
                value_x: str = match.package_x.get_value(value_type)
                value_y: str = match.package_y.get_value(value_type)
                table.add_row([
                    match.directory_path,
                    match.package_x.name,
                    value_x,
                    value_y if is_equal else Console.alert(value_y)
                ])
            print(table.render())

        if Console.TYPE_REPLACE == console.get_type():
            lock_modifier: LockModifier = LockModifier(args.config)
            value_type: List[str] = ["source", "reference"]
            package_names: List[str] = self.get_package_names()
            matches: List[Match] = self.get_matches(args.config)
            matches_not_equal: List[Match] = self.get_not_equal(matches, value_type)
            packages_not_equal: List[str] = []
            for match in matches_not_equal:
                if match.package_x.name in package_names:
                    packages_not_equal.append(match.package_x.name)
            if not packages_not_equal:
                print(Console.success("Nothing to update, all sha are valid"))
            else:
                selected_packages: List[str] = console.select_packages(packages_not_equal)
                if not selected_packages:
                    print(Console.warning("No selected packages, abort"))
                else:
                    table: Table = Table(["Directory", "Package", "Status", "Message"])
                    if not args.all:
                        matches: List[Match] = self.get_not_equal(matches, value_type)
                    for match in matches:
                        if match.package_x.name in selected_packages:
                            result: Result = lock_modifier.update_package(match, value_type)
                            table.add_row([
                                result.directory,
                                result.package,
                                result.status,
                                result.message
                            ])
                    print(table.render())

        if Console.TYPE_FETCH == console.get_type():
            client: Client = self.get_client()
            data = self.yaml_parser.get_data()
            yaml_replacer: YamlReplacer = YamlReplacer()
            packages: Collection = self.yaml_parser.get_packages()
            selected_packages: List[str] = console.select_packages(self.get_package_names())
            filtered_packages: List[Package] = packages.find_by_names(selected_packages)
            if not filtered_packages:
                print(Console.warning("No selected packages, abort"))
            else:
                for package in filtered_packages:
                    sha: str = client.get_last_sha(package.repository, package.branch)
                    if sha != package.get_value(["source", "reference"]):
                        yaml_replacer.replace_value(data, sha, ["packages", package.name, "source", "reference"])
                self.yaml_parser.save(data)

        sys.exit()

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

    def get_repository_names(self) -> List[str]:
        packages: Collection = self.yaml_parser.get_packages()
        repository_names: List[str] = []
        for package in packages:
            repository_names.append(package.repository)
        return repository_names

    def get_client(self) -> Client:
        auth: Auth = Auth()
        auth.parse_yaml(self.yaml_parser)
        return Client(auth)
