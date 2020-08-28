import argparse
from classes.console.abstract_console import AbstractConsole
from classes.console.console_theme import QuestionTheme
from inquirer import Checkbox, List as Radio, prompt
from typing import Any, Dict, Iterator, List, Optional


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
        parser.add_argument("option", type=str, help="Available options: fetch, replace, search")
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

    def select_packages(self, choices: Iterator[Any]) -> List[Any]:
        questions: List[Checkbox] = []
        checkbox: Checkbox = Checkbox(
            "packages",
            message="What packages do you want to update?",
            choices=choices
        )
        questions.append(checkbox)
        answers: Dict[str] = prompt(questions, theme=QuestionTheme())
        return answers["packages"] if answers and "packages" in answers else []

    def confirm_binary(self, message: str) -> Optional[bool]:
        questions: List[Radio] = []
        radio: Radio = Radio(
            "confirmation",
            message=message,
            choices=[("Yes", True), ("No", False)],
        )
        questions.append(radio)
        answers: Dict[str] = prompt(questions, theme=QuestionTheme())
        return answers["confirmation"] if answers and "confirmation" in answers else None
