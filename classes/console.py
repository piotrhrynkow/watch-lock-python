import argparse
from classes.abstract_console import AbstractConsole


class Console(AbstractConsole):

    @staticmethod
    def init():
        parser = argparse.ArgumentParser(description='Find wrong references in locks')
        parser.add_argument('-a', '--all', action='store_true', help='Show all matches')
        parser.add_argument('-c', '--config', type=str, default='config.yaml', help='Config path')
        parser.add_argument('-j', '--json', action='store_true', help='Check if package exists in composer.json')

        return parser.parse_args()
