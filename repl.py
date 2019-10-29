import cmd
import sys


class REPL(cmd.Cmd):
    metacommands = ("exit",)
    select_statement = "select"
    insert_statement = "insert"
    meta_prefix = "."
    intro = "Welcome to the pysql shell. Type help or ? to list commands.\n"
    prompt = "(pysql) "

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
        elif line.startswith(self.insert_statement):
            print(f"Executing insert statement {line}")
        else:
            print(f"Unrecognized statement {line}")


if __name__ == "__main__":
    REPL().cmdloop()
