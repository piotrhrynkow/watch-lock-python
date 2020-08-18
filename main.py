from classes.console import Console
from classes.matcher import Matcher
from classes.table import Table
from model.match import Match


if __name__ == '__main__':

    args = Console.init()

    table = Table()
    table.set_header(["File", "Name", "Reference expected", "Reference actual"])
    matches = Matcher.get_matches(args.config)
    for match in matches:
        value_type = ["source", "reference"]
        is_equal = match.is_equal(value_type)
        if not is_equal or args.all:
            value_x = Match.get_value(match.package_x, value_type)
            value_y = Match.get_value(match.package_y, value_type)
            table.add_row([
                match.file_path,
                match.package_x.name,
                value_x,
                value_y if is_equal else Console.alert(value_y)
            ])
    table.print()
