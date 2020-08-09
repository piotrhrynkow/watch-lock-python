from tabulate import tabulate


class Table:

    def __init__(self):
        self.header = []
        self.rows = []
        self.style = "psql"

    def set_header(self, header):
        self.header = header

    def add_row(self, row):
        self.rows.append(row)

    def print(self):
        print(tabulate(self.rows, headers=self.header, tablefmt=self.style))
