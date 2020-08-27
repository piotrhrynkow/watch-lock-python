import json
from pathlib import Path
from typing import List
from classes.model.package import Package


class JsonParser:

    @staticmethod
    def get_names(path: Path) -> List[str]:
        names = []
        data = JsonParser.get_data(path)
        groups = ["require", "require-dev"]
        for group in groups:
            if group in data:
                for name in data[group]:
                    names.append(name)
        return names

    @staticmethod
    def get_packages(path: Path) -> List[Package]:
        packages: List[Package] = []
        data = JsonParser.get_data(path)
        packages_data = []
        groups = ["packages", "packages-dev"]
        for group in groups:
            if group in data:
                packages_data += data[group]
        for package in packages_data:
            packages.append(Package(package["name"], package))
        return packages

    @staticmethod
    def get_data(path: Path):
        stream = path.open()
        data = json.loads(stream.read())
        return data
