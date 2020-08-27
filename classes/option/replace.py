from classes.console.console import Console
from classes.lock_modifier.lock_modifier import LockModifier
from classes.lock_modifier.result import Result as LockResult
from classes.option.abstract_option import AbstractOption
from classes.table import Table
from classes.package_matcher.match import Match
from typing import Iterator, List, Tuple


class OptionReplace(AbstractOption):

    def run(self) -> None:
        lock_modifier: LockModifier = LockModifier(self.args.config)
        value_type: List[str] = ["source", "reference"]
        package_names: Iterator[str] = self.get_package_names()
        matches: List[Match] = self.get_matches(self.args.config)
        matches_not_equal: List[Match] = list(filter(lambda match: not match.is_equal(value_type), matches))
        if not sum(match.package_x.name in package_names for match in matches_not_equal):
            print(Console.success("Nothing to update, all sha are valid"))
        else:
            choices: List[Tuple[str, Match]] = self.__prepare_choices(matches_not_equal)
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
                        self.__color_status(result.status),
                        result.message
                    ])
                print(table.render())

    @staticmethod
    def __prepare_choices(matches: List[Match]) -> List[Tuple[str, Match]]:
        choices: List[Tuple[str, Match]] = []
        for match in matches:
            choices.append((
                "{package} - ({path})".format(package=match.package_x.name, path=match.directory_path),
                match
            ))
        return choices

    @staticmethod
    def __color_status(status: str) -> str:
        if LockResult.STATUS_SUCCESS == status:
            return Console.success(status)
        if LockResult.STATUS_WARNING == status:
            return Console.warning(status)
        if LockResult.STATUS_FAILED == status:
            return Console.alert(status)
        return status
