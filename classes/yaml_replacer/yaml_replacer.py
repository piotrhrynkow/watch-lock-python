from classes.github.client import Client
from classes.yaml_parser import YamlParser
from classes.yaml_replacer.result import Result
from classes.model.package import Package
from typing import Any, List, Optional


class YamlReplacer:

    def __init__(self, client: Client, yaml_parser: YamlParser):
        self.client: Client = client
        self.yaml_parser: YamlParser = yaml_parser

    def replace_sha(self, packages: List[Package]) -> List[Result]:
        results: List[Result] = []
        data = self.yaml_parser.get_data()
        for package in packages:
            result: Result = Result(package.name)
            current_sha: str = package.get_value(["source", "reference"])
            result.set_sha_before(current_sha)
            fetched_sha: str = self.client.get_last_sha(package.repository, package.branch)
            try:
                result.set_sha_after(fetched_sha)
                if fetched_sha != current_sha:
                    self.replace_value(data, fetched_sha, ["packages", package.name, "source", "reference"])
                    result.set_success()
                else:
                    result.set_ignored("Current sha, no required action")
            except Exception as exception:
                result.set_failed(self.__get_exception_message(exception))
            results.append(result)
        self.yaml_parser.save(data)
        return results

    @staticmethod
    def replace_value(data: Any, value: str, fields: List[str]) -> Any:
        if fields:
            field: str = fields.pop(0)
            data[field] = YamlReplacer.replace_value(data[field], value, fields)
            return data
        return value

    @staticmethod
    def __get_exception_message(exception: Exception) -> Optional[str]:
        return exception.message if hasattr(exception, 'message') else None
