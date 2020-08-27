from typing import Any, Callable, Dict, Iterator, List, Union


class Collection:

    @staticmethod
    def filter_single(collection: List[Any], function: Callable) -> Any:
        return next(filter(function, collection), None)

    @staticmethod
    def get_single_by(collection: List[Any], property: str, value: Any) -> Any:
        return Collection.filter_single(collection, lambda item: Collection.__get_value(item, property) == value)

    @staticmethod
    def get_values(collection: List[Any], property: str) -> Iterator:
        return map(lambda item: Collection.__get_value(item, property), collection)

    @staticmethod
    def __get_value(item: Any, property: str) -> Any:
        return item[property] if isinstance(item, Dict) else getattr(item, property)
