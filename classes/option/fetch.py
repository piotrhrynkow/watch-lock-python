from classes.console.console import Console
from classes.github.client import Client
from classes.option.abstract_option import AbstractOption
from classes.table import Table
from classes.yaml_replacer.result import Result as YamlResult
from classes.yaml_replacer.yaml_replacer import YamlReplacer
from classes.model.package import Package
from typing import List


class OptionFetch(AbstractOption):

    def run(self) -> None:
        packages: List[Package] = self.yaml_parser.get_packages()
        selected_packages: List[str] = self.console.select_packages(list(self.get_package_names()))
        filtered_packages: List[Package] = list(filter(lambda package: package.name in selected_packages, packages))
        if not filtered_packages:
            print(Console.warning("No selected packages, abort"))
        else:
            client: Client = self.get_client()
            yaml_replacer: YamlReplacer = YamlReplacer(client, self.yaml_parser)
            results: List[YamlResult] = yaml_replacer.replace_sha(filtered_packages)
            table: Table = Table(["Package", "Before", "After", "Status", "Message"])
            for result in results:
                table.add_row([
                    result.package,
                    result.sha_before,
                    result.sha_after,
                    self.__color_status(result.status),
                    result.message
                ])
            print(table.render())

    @staticmethod
    def __color_status(status: str) -> str:
        if YamlResult.STATUS_SUCCESS == status:
            return Console.success(status)
        if YamlResult.STATUS_FAILED == status:
            return Console.alert(status)
        return status
