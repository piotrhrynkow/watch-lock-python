import json
import glob
from pathlib import Path
from typing import List
from classes.console import Console
from classes.table import Table
from classes.yaml_parser import YamlParser
from model.match import Match
from model.package import Package
from model.package_collection import Collection


class JsonParser:

    @staticmethod
    def get_names(path: Path) -> List[str]:
        names = []
        stream = path.open()
        data = json.loads(stream.read())
        groups = ["require", "require-dev"]
        for group in groups:
            if group in data:
                for name in data[group]:
                    names.append(name)
        return names

    @staticmethod
    def get_packages(path: Path) -> Collection:
        packages = Collection()
        stream = path.open()
        data = json.loads(stream.read())
        packages_data = []
        groups = ["packages", "packages-dev"]
        for group in groups:
            if group in data:
                packages_data += data[group]
        for package in packages_data:
            packages.add(Package(package["name"], package))
        return packages


class FileFinder:

    @staticmethod
    def get_file_paths(directory: str, extension: str) -> List[Path]:
        lock_files = []
        lock_paths = glob.glob(directory + "/composer." + extension, recursive=True)
        for file in lock_paths:
            lock_files.append(Path(file))
        return lock_files

    @staticmethod
    def get_lock_path(json_path) -> Path:
        return json_path.joinpath(json_path.parent, "composer.lock")


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
