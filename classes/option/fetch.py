from classes.console import Console
from classes.github.client import Client
from classes.option.abstract_option import AbstractOption
from classes.table import Table
from classes.yaml_replacer.result import Result as YamlResult
from classes.yaml_replacer.yaml_replacer import YamlReplacer
from model.package import Package
from model.package_collection import Collection
from typing import List


class OptionFetch(AbstractOption):

    def run(self) -> None:
        packages: Collection = self.yaml_parser.get_packages()
        selected_packages: List[str] = self.console.select_packages(self.get_package_names())
        filtered_packages: List[Package] = packages.find_by_names(selected_packages)
        if not filtered_packages:
            print(Console.warning("No selected packages, abort"))
        else:
            client: Client = self.get_client()
            yaml_replacer: YamlReplacer = YamlReplacer(client, self.yaml_parser)
            results: List[YamlResult] = yaml_replacer.replace_sha(filtered_packages)
            table: Table = Table(["Package", "Before", "After", "Status", "Message"])
            for result in results:
                table.add_row([result.package, result.sha_before, result.sha_after, result.status, result.message])
            print(table.render())
