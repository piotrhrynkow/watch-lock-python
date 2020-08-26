import argparse
from classes.abstract_console import AbstractConsole
from classes.console_theme import QuestionTheme
from inquirer import Checkbox, prompt
from typing import List, Any


class Console(AbstractConsole):

    OPTION_FETCH = "fetch"
    OPTION_REPLACE = "replace"
    OPTION_SEARCH = "search"

    def __init__(self):
        self.args = None
        parser: argparse.ArgumentParser = self.create_parser(False)
        option: str = parser.parse_known_args()[0].option
        self.parser: argparse.ArgumentParser = self.create_parser(True)
        if self.OPTION_SEARCH == option:
            self.search_arguments()

    def create_parser(self, has_help: bool) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Find wrong references in locks", add_help=has_help)
        parser.add_argument("option", type=str, help="Option")
        parser.add_argument("-c", "--config", type=str, default="config.yaml", help="Config path")
        parser.add_argument("-j", "--json", action="store_true", help="Check if package exists in composer.json")
        return parser

    def search_arguments(self):
        self.parser.add_argument("-a", "--all", action="store_true", help="Show all matches")

    def get_option(self) -> str:
        return self.get_args().option

    def get_args(self):
        if self.args is None:
            self.args = self.parser.parse_args()
        return self.args

    def select_packages(self, choices: List[Any]) -> List[Any]:
        questions: List[Checkbox] = []
        checkbox: Checkbox = Checkbox(
            "packages",
            message="What packages do you want to update?",
            choices=choices
        )
        questions.append(checkbox)
        answers = prompt(questions, theme=QuestionTheme())
        return answers["packages"] if answers and "packages" in answers else []
