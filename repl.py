import cmd
import sys
from dataclasses import dataclass


@dataclass
class TableRowDef:
    id: int
    username: str
    email: str

class InmemTable:
    __row_def = TableRowDef

    def __init__(self):
        self.__rows = []

    def insert(self, insert_args: tuple):
        self.__rows.append(self.__row_def(*insert_args))

    def select(self):
        for row in self.__rows:
            print(row)

    def clear_table(self):
        self.__rows = []

class REPL(cmd.Cmd):
    metacommands = ("exit", "help")
    select_statement = "select"
    insert_statement = "insert"
    meta_prefix = "."
    intro = "Welcome to the pysql shell. Type help or ? to list commands.\n"
    prompt = "(pysql) "
    table = InmemTable()

    def do_exit(self, arg):
        "Exits the REPL"
        raise sys.exit(0)

    def do_help(self, arg):
        "Print help"
        print('This is help')


    def onecmd(self, line):
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        if line == 'EOF' :
            self.lastcmd = ''
        if line == '':
            return self.default(line)
        else:
            if line.startswith(self.meta_prefix):
                if line[1:] in self.metacommands:
                    line = line[1:]
                try:
                    func = getattr(self, 'do_' + line)
                except AttributeError:
                    return self.default(line)
                return func(arg)
            else:
                self.parse_statement(line)

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
