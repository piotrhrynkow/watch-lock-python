from classes.console import Console
from classes.lock_modifier.lock_modifier import LockModifier
from classes.lock_modifier.result import Result as LockResult
from classes.option.abstract_option import AbstractOption
from classes.table import Table
from model.match import Match
from typing import List, Tuple


class OptionReplace(AbstractOption):

    def run(self) -> None:
        lock_modifier: LockModifier = LockModifier(self.args.config)
        value_type: List[str] = ["source", "reference"]
        package_names: List[str] = self.get_package_names()
        matches: List[Match] = self.get_matches(self.args.config)
        matches_not_equal: List[Match] = self.get_not_equal(matches, value_type)
        packages_not_equal: List[str] = []
        for match in matches_not_equal:
            if match.package_x.name in package_names:
                packages_not_equal.append(match.package_x.name)
        if not packages_not_equal:
            print(Console.success("Nothing to update, all sha are valid"))
        else:
            choices: List[Tuple[str, Match]] = []
            for match in matches_not_equal:
                choices.append((
                    "{package} - ({path})".format(package=match.package_x.name, path=match.directory_path),
                    match
                ))
            selected_matches: List[Match] = self.console.select_packages(choices)
            if not selected_matches:
                print(Console.warning("No selected packages, abort"))
            else:
                table: Table = Table(["Directory", "Package", "Status", "Message"])
                for match in selected_matches:
                    result: LockResult = lock_modifier.update_package(match, value_type)
                    table.add_row([
                        result.directory,
                        result.package,
                        result.status,
                        result.message
                    ])
                print(table.render())
