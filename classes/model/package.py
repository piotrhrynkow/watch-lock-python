from classes.util.tree import Tree
from typing import Any, Dict, List, Optional, Union


class Package:

    def __init__(self, name: str, values):
        self.name: str = name
        self.values: Dict[Any] = values
        self.repository: Optional[str] = self.get_value("repository")
        self.branch: Optional[str] = self.get_value("branch")

    def get_value(self, keys: Union[str, List[str]]) -> Any:
        return Tree.get_value(self.values, keys)
