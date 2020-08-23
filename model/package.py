from typing import Any, List, Optional, Union


class Package:

    def __init__(self, name: str, values):
        self.name: str = name
        self.values: List[Any] = values
        self.repository: Optional[str] = self.get_value("repository")
        self.branch: Optional[str] = self.get_value("branch")

    def get_value(self, fields: Union[str, List[str]]):
        if isinstance(fields, str):
            fields = [fields]
        value = self.values
        try:
            for field in fields:
                value = value[field]
            return value
        except KeyError:
            return None
