from abc import ABC, abstractmethod
from classes.console import Console
from classes.yaml_parser import YamlParser


class OptionInterface(ABC):

    @abstractmethod
    def __init__(self, console: Console, yaml_parser: YamlParser):
        """Constructor"""
        pass

    @abstractmethod
    def run(self) -> None:
        """Implement method responsible for executing class logic"""
        pass
