from classes.model.package import Package
from pathlib import Path
from typing import List


class Match:

    def __init__(self, file_path: Path, package_x: Package, package_y: Package):
        self.lock_path: Path = file_path
        self.directory_path: Path = file_path.parent
        self.package_x: Package = package_x
        self.package_y: Package = package_y

    def is_equal(self, fields: List[str]) -> bool:
        return self.package_x.get_value(fields) == self.package_y.get_value(fields)
