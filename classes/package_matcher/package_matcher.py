from classes.file_finder import FileFinder
from classes.json_parser import JsonParser
from classes.util.collection import Collection
from classes.yaml_parser import YamlParser
from classes.package_matcher.match import Match
from classes.model.package import Package
from pathlib import Path
from typing import List, Optional


class PackageMatcher:

    @staticmethod
    def get_json_matches(config_path: str) -> List[Match]:
        matches: List[Match] = []
        yaml: YamlParser = YamlParser(config_path)
        for directory in yaml.get_directories():
            yaml_packages: List[Package] = yaml.get_packages()
            json_paths: List[Path] = FileFinder.get_file_paths(directory, "json")
            for json_path in json_paths:
                for json_package_name in JsonParser.get_names(json_path):
                    yaml_package: Optional[Package] = Collection.get_single_by(yaml_packages, "name", json_package_name)
                    if yaml_package is not None:
                        lock_path: Path = FileFinder.get_lock_path(json_path)
                        for lock_package in JsonParser.get_packages(lock_path.absolute()):
                            if lock_package.name == json_package_name:
                                matches.append(Match(lock_path.resolve(), yaml_package, lock_package))
                                break
        return matches

    @staticmethod
    def get_lock_matches(config_path: str) -> List[Match]:
        matches: List[Match] = []
        yaml: YamlParser = YamlParser(config_path)
        for directory in yaml.get_directories():
            yaml_packages: List[Package] = yaml.get_packages()
            lock_paths: List[Path] = FileFinder.get_file_paths(directory, "lock")
            for lock_path in lock_paths:
                for lock_package in JsonParser.get_packages(lock_path.absolute()):
                    yaml_package: Optional[Package] = Collection.get_single_by(yaml_packages, "name", lock_package.name)
                    if yaml_package is not None and lock_package.name == yaml_package.name:
                        matches.append(Match(lock_path.resolve(), yaml_package, lock_package))
        return matches
