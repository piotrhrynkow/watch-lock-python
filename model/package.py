from typing import List


class Package:

    def __init__(self, name, values):
        self.name: str = name
        self.values: List = values

    def get_value(self, fields: List[str]):
        value = self.values
        for field in fields:
            value = value[field]
        return value
