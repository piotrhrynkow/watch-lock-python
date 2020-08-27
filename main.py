from classes.console.console import Console
from classes.option.fetch import OptionFetch
from classes.option.option_interface import OptionInterface
from classes.option.replace import OptionReplace
from classes.option.search import OptionSearch
from classes.yaml_parser import YamlParser
import sys
from typing import Any


if __name__ == '__main__':

    console: Console = Console()
    args: Any = console.get_args()
    yaml_parser: YamlParser = YamlParser(args.config)

    if Console.OPTION_SEARCH == console.get_option():
        option: OptionInterface = OptionSearch(console, yaml_parser)
    elif Console.OPTION_REPLACE == console.get_option():
        option: OptionInterface = OptionReplace(console, yaml_parser)
    elif Console.OPTION_FETCH == console.get_option():
        option: OptionInterface = OptionFetch(console, yaml_parser)
    else:
        print(Console.warning("Choose correct option, abort"))
        sys.exit()
    option.run()

    sys.exit()
