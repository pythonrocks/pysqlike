import cmd
import sys
import pickle
import struct
from dataclasses import dataclass


class Cursor:

    def __init__(self, table):
        self.table = table
        self.row_num = 0
        self.last_row = self.is_last_row()

    def table_start(self):
        self.row_num = 0
        self.last_row = self.is_last_row()

    def table_end(self):
        self.row_num = table.num_rows - 1 if table.num_rows else 0
        self.last_row = True

    def is_last_row(self):
        return self.row_num == (self.table.num_rows - 1)

    def advance_row(self):
        self.row_num += 1
        self.last_row = self.is_last_row()

    def cursor_value(self):
        return self.table[self.row_num]

    # def __getitem__(self):
    #     return self.table[self.row_num]

    def __iter__(self):
        return self

    def __next__(self):
        if self.row_num >= self.table.num_rows:
            raise StopIteration
        row = self.cursor_value()
        self.advance_row()
        return row


@dataclass
class TableRowDef:
    id: int
    username: str
    email: str

class InmemTable:
    # __row_struct = struct.pack('lss')
    __row_def = TableRowDef
    __filename = 'table.psl'

    def get_cursor(self):
        return Cursor(self)

    def __init__(self):
        self.__rows = []

    def __getitem__(self, index):
        return self.__rows[index]

    @property
    def num_rows(self):
        return len(self.__rows)

    def insert(self, insert_args: tuple):
        self.__rows.append(self.__row_def(*insert_args))

    def select(self):
        for row in self.get_cursor():
            print(row)

    def clear_table(self):
        self.__rows = []

    def save(self):
        with open(self.__filename, 'wb') as fp:
            pickle.dump(self.__rows, fp, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        try:
            with open(self.__filename, 'rb') as fp:
                self.__rows = pickle.load(fp)
        except FileNotFoundError:
            self.__rows = []

class REPL(cmd.Cmd):
    metacommands = ("exit",)
    select_statement = "select"
    insert_statement = "insert"
    meta_prefix = "."
    intro = "Welcome to the pysql shell. Type help or ? to list commands.\n"
    prompt = "(pysql) "
    table = InmemTable()

    def preloop(self):
        self.table.load()

    def postloop(self):
        self.table.save()

    def do_exit(self, arg):
        "Exits the REPL"
        raise sys.exit(0)

    def onecmd(self, line):
        if line.startswith(self.meta_prefix):
            if line[1:] in self.metacommands:
                line = line[1:]
                return True
            else:
                print(f"Command not recognized {line}")
                return False
        else:
            self.parse_statement(line)
        return False

    def precmd(self, line):
        return line.lower().strip()

    def default(self, line):
        print(
            f"Unrecognized command {line}. Type ? or help to see the list of commands."
        )

    def parse_statement(self, line):
        if line.startswith(self.select_statement):
            print(f"Executing select statement {line}")
            self.table.select()
        elif line.startswith(self.insert_statement):
            print(f"Executing insert statement {line}")
            insert_args = line.split()[1:]
            if len(insert_args) != 3:
                raise ValueError("Invalid insert parameter")
            row = (int(insert_args[0]), *insert_args[1:])
            self.table.insert(row)
        else:
            print(f"Unrecognized statement {line}")


if __name__ == "__main__":
    REPL().cmdloop()
