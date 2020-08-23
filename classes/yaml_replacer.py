from typing import Any, List


class YamlReplacer:

    @staticmethod
    def replace_value(data: Any, value: str, fields: List[str]) -> Any:
        if fields:
            field: str = fields.pop(0)
            data[field] = YamlReplacer.replace_value(data[field], value, fields)
            return data
        return value
