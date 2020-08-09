class Collection:

    def __init__(self):
        self.packages = []

    def __iter__(self):
        self.index = 0
        self.packages_length = len(self.packages)
        return self

    def __next__(self):
        if self.index == self.packages_length:
            raise StopIteration
        package = self.packages[self.index]
        self.index += 1
        return package

    def add(self, package):
        self.packages.append(package)

    def find_by_name(self, name):
        for package in self.packages:
            if package.name == name:
                return package
        return None
