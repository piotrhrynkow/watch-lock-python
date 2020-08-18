from classes.file_finder import FileFinder
from classes.json_matcher import JsonParser
from classes.yaml_parser import YamlParser
from model.match import Match
from typing import List


class Matcher:

    @staticmethod
    def get_matches(config_path: str) -> List[Match]:
        matches = []
        yaml = YamlParser(config_path)
        for directory in yaml.get_directories():
            yaml_packages = yaml.get_packages()
            json_paths = FileFinder.get_file_paths(directory, "json")
            for json_path in json_paths:
                for json_package_name in JsonParser.get_names(json_path):
                    yaml_package = yaml_packages.find_by_name(json_package_name)
                    if yaml_package is not None:
                        lock_path = FileFinder.get_lock_path(json_path)
                        for lock_package in JsonParser.get_packages(lock_path.absolute()):
                            if lock_package.name == json_package_name:
                                matches.append(Match(lock_path.resolve().parent, yaml_package, lock_package))
                                break
        return matches
