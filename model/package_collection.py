from typing import List, Optional
from model.package import Package


class Collection:

    def __init__(self):
        self.packages: List[Package] = []

    def __iter__(self):
        self.index: int = 0
        self.packages_length = len(self.packages)
        return self

    def __next__(self) -> Package:
        if self.index == self.packages_length:
            raise StopIteration
        package: Package = self.packages[self.index]
        self.index += 1
        return package

    def add(self, package: Package):
        self.packages.append(package)

    def find_by_name(self, name: str) -> Optional[Package]:
        for package in self.packages:
            if package.name == name:
                return package
        return None
