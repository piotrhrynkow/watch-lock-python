from classes.console import Console
from classes.lock_modifier.lock_modifier import LockModifier
from classes.lock_modifier.result import Result
from classes.matcher import Matcher
from classes.table import Table
from classes.yaml_parser import YamlParser
from model.match import Match
from model.package_collection import Collection
import sys
from typing import List


class Main:

    def __init__(self):
        console = Console()

        if Console.TYPE_SEARCH == console.get_type():
            args = console.get_args()
            table: Table = Table(["File", "Name", "Reference expected", "Reference actual"])
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
            args = console.get_args()
            table: Table = Table(["Directory", "Status", "Message"])
            lock_modifier: LockModifier = LockModifier(args.config)
            value_type: List[str] = ["source", "reference"]
            package_names: List[str] = self.get_package_names(args.config)
            matches: List[Match] = self.get_matches(args.config)
            matches_not_equal: List[Match] = self.get_not_equal(matches, value_type)
            packages_not_equal: List[str] = []
            for match in matches_not_equal:
                if match.package_x.name in package_names:
                    packages_not_equal.append(match.package_x.name)
            if 0 == len(packages_not_equal):
                print(Console.success("Nothing to update, all hashes are valid"))
            else:
                selected_packages: List[str] = console.select_packages(packages_not_equal)
                if 0 == len(selected_packages):
                    print(Console.warning("No selected packages, abort"))
                else:
                    if not args.all:
                        matches: List[Match] = self.get_not_equal(matches, value_type)
                    for match in matches:
                        if match.package_x.name in selected_packages:
                            result: Result = lock_modifier.update_package(match, value_type)
                            table.add_row([
                                result.directory,
                                result.status,
                                result.message
                            ])
                    print(table.render())

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

    @staticmethod
    def get_package_names(config_path: str):
        yaml: YamlParser = YamlParser(config_path)
        packages: Collection = yaml.get_packages()
        package_names: List[str] = []
        for package in packages:
            package_names.append(package.name)
        return package_names
