from classes.console import Console
from classes.lock_modifier.lock_modifier import LockModifier
from classes.lock_modifier.result import Result
from classes.matcher import Matcher
from classes.table import Table
from model.match import Match
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
                matches: List[Match] = self.get_no_equal(matches, value_type)
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
            matches: List[Match] = self.get_matches(args.config)
            if not args.all:
                matches: List[Match] = self.get_no_equal(matches, value_type)
            for match in matches:
                if match.package_x.name == args.package:
                    result: Result = lock_modifier.update_package(match, value_type)
                    table.add_row([
                        result.directory,
                        result.status,
                        result.message
                    ])
            print(table.render())

    @staticmethod
    def get_matches(config: str, json: bool = False) -> List[Match]:
        return Matcher.get_json_matches(config) if json else Matcher.get_lock_matches(config)

    @staticmethod
    def get_no_equal(matches: List[Match], fields: List[str]) -> List[Match]:
        filtered: List[Match] = []
        for match in matches:
            if not match.is_equal(fields):
                filtered.append(match)
        return filtered
