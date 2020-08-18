import json
from pathlib import Path
from typing import List
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
