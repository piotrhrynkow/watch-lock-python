from classes.model.package import Package
import json
from pathlib import Path
from typing import Any, IO, List


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
    def get_data(path: Path) -> Any:
        stream: IO = path.open(encoding="utf8")
        data: Any = json.loads(stream.read())
        stream.close()
        return data
