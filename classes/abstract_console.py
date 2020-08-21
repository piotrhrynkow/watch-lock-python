from abc import ABC
from colorama import Fore, Style


class AbstractConsole(ABC):

    @staticmethod
    def color(color: str, text: str) -> str:
        return color + text + Style.RESET_ALL

    @staticmethod
    def alert(text: str) -> str:
        return AbstractConsole.color(Fore.RED, text)

    @staticmethod
    def warning(text: str) -> str:
        return AbstractConsole.color(Fore.YELLOW, text)