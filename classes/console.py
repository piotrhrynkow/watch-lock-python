import argparse
from classes.abstract_console import AbstractConsole
from classes.console_theme import QuestionTheme
from inquirer import Checkbox, prompt
from typing import List


class Console(AbstractConsole):

    TYPE_REPLACE = "replace"
    TYPE_SEARCH = "search"

    def __init__(self):
        self.args = None
        parser: argparse.ArgumentParser = self.create_parser(False)
        type: str = parser.parse_known_args()[0].type
        self.parser: argparse.ArgumentParser = self.create_parser(True)

    def create_parser(self, has_help: bool) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Find wrong references in locks", add_help=has_help)
        parser.add_argument("type", type=str, help="Type")
        parser.add_argument("-c", "--config", type=str, default="config.yaml", help="Config path")
        parser.add_argument("-j", "--json", action="store_true", help="Check if package exists in composer.json")
        parser.add_argument("-a", "--all", action="store_true", help="Show all matches")
        return parser

    def get_type(self) -> str:
        return self.get_args().type

    def get_args(self):
        if self.args is None:
            self.args = self.parser.parse_args()
        return self.args

    def select_packages(self, packages: List[str]) -> List[str]:
        questions: List[Checkbox] = []
        checkbox: Checkbox = Checkbox(
            "packages",
            message="What packages do you want to update?",
            choices=packages
        )
        questions.append(checkbox)
        answers = prompt(questions, theme=QuestionTheme())
        return answers["packages"] if "packages" in answers else []
