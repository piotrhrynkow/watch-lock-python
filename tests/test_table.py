from classes.table import Table
from typing import IO


def test_table_print():
    table: Table = Table(["Header 1", "Header 2", "Header 3"])
    table.add_row(["Row 1-1", "Row 1-2", "Row 1-3"])
    table.add_row(["Row 2-1", "Row 2-2", "Row 2-3"])
    table.add_row(["Row 3-1", "Row 3-2", "Row 3-3"])
    data: str = get_table_fixture()
    assert table.render() == data


def get_table_fixture() -> str:
    stream: IO = open("tests/data/table/data.txt", "r")
    data = stream.read()
    stream.close()
    return data

