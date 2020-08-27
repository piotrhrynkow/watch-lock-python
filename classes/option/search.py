from classes.console.console import Console
from classes.option.abstract_option import AbstractOption
from classes.table import Table
from classes.package_matcher.match import Match
from typing import Iterator, List


class OptionSearch(AbstractOption):

    def run(self) -> None:
        table: Table = Table(["Directory", "Name", "Reference expected", "Reference actual"])
        value_type: List[str] = ["source", "reference"]
        matches: List[Match] = self.get_matches(self.args.config)
        if not self.args.all:
            matches: Iterator[Match] = filter(lambda match: not match.is_equal(value_type), matches)
        for match in matches:
            is_equal: bool = match.is_equal(value_type)
            value_x: str = match.package_x.get_value(value_type)
            value_y: str = match.package_y.get_value(value_type)
            table.add_row([
                match.directory_path,
                match.package_name,
                value_x,
                value_y if is_equal else Console.alert(value_y)
            ])
        print(table.render())
