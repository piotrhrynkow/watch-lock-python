from model.package import Package
from model.package_collection import Collection
from pathlib import Path
from typing import List
import yaml


class YamlParser:

    def __init__(self, path: str):
        self.path = path
        self.data = None

    def __get_data(self):
        if self.data is None:
            file_path = Path(self.path)
            if not file_path.exists():
                raise Exception("Unable to find file \"{}\"".format(self.path))
            if not file_path.is_file():
                raise Exception("Path \"{}\" is not file".format(file_path.resolve()))
            stream = file_path.open("r")
            self.data = yaml.safe_load(stream)
        return self.data

    def get_directories(self) -> List[str]:
        data = self.__get_data()
        return data["directories"]

    def get_packages(self) -> Collection:
        packages = Collection()
        data = self.__get_data()
        for name, values in data["packages"].items():
            packages.add(Package(name, values))
        return packages
