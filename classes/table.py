from tabulate import tabulate
from typing import List


class Table:

    def __init__(self, header: List[str] = []):
        self.header: List[str] = header
        self.rows: List[List[str]] = []
        self.style: str = "psql"

    def set_header(self, header: List[str]):
        self.header = header

    def add_row(self, row: List[str]):
        self.rows.append(row)

    def render(self) -> str:
        return tabulate(self.rows, headers=self.header, tablefmt=self.style)
