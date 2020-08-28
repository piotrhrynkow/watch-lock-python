from classes.model.package import Package
from classes.util.tree import Tree
from pathlib import Path
from typing import Any, Dict, IO, List, Optional, Union
import yaml


class YamlParser:

    def __init__(self, path: str):
        self.path: str = path
        self.data: Optional[Dict[str, Any]] = None

    def __valid_path(self):
        file_path = Path(self.path)
        if not file_path.exists():
            raise Exception("Unable to find file \"{}\"".format(self.path))
        if not file_path.is_file():
            raise Exception("Path \"{}\" is not file".format(file_path.resolve()))

    def get_data(self) -> Dict[str, Any]:
        if self.data is None:
            self.__valid_path()
            file_path: Path = Path(self.path)
            stream: IO = file_path.open("r")
            self.data = yaml.safe_load(stream)
            stream.close()
        return self.data

    def get_directories(self) -> List[str]:
        data: Dict[str, Any] = self.get_data()
        return data["directories"]

    def get_packages(self) -> List[Package]:
        packages: List[Package] = []
        data: Dict[str, Any] = self.get_data()
        for name, values in data["packages"].items():
            packages.append(Package(name, values))
        return packages

    def get_value(self, keys: Union[str, List[str]]):
        return Tree.get_value(self.get_data(), keys)

    def get_repositories(self) -> List[str]:
        repositories: List[str] = []
        packages: List[Package] = self.get_packages()
        for package in packages:
            repositories.append(package.repository)
        return repositories

    def get_token(self) -> Optional[str]:
        return self.get_value(["api", "token"])

    def get_login(self) -> Optional[str]:
        return self.get_value(["api", "login"])

    def get_password(self) -> Optional[str]:
        return self.get_value(["api", "password"])

    def get_url(self) -> Optional[str]:
        return self.get_value(["api", "url"])

    def save(self, data):
        self.__valid_path()
        file_path: Path = Path(self.path)
        stream: IO = file_path.open("w")
        yaml.dump(data, stream)
        stream.close()
