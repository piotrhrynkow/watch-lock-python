from model.package import Package


class Match:

    def __init__(self, file_path, package_x, package_y):
        self.file_path = file_path
        self.package_x = package_x
        self.package_y = package_y

    def is_equal(self, fields) -> bool:
        return self.get_value(self.package_x, fields) == self.get_value(self.package_y, fields)

    @staticmethod
    def get_value(package: Package, fields):
        value = package.values
        for field in fields:
            value = value[field]
        return value
