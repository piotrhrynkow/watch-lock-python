from typing import Any, List, Union


class Tree:

    @staticmethod
    def get_value(tree: Any, keys: Union[str, List[str]]) -> Any:
        if isinstance(keys, str):
            keys: List[str] = [keys]
        value: Any = tree
        try:
            for key in keys:
                value = value[key]
            return value
        except KeyError:
            return None
