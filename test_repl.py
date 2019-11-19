import pexpect
from repl import TableRowDef
import pytest

REPL_PROMPT = "\\(pysql\\) "


@pytest.fixture(autouse=True)
def child():
    child_p = pexpect.spawn(".venv/bin/python repl.py", timeout=5)
    child_p.expect(REPL_PROMPT)
    yield child_p
    child_p.kill(9)


def test_insert(child):
    insert_line = "insert 1 aaa bbb"
    # import ipdb; ipdb.set_trace()
    child.sendline(insert_line)
    child.expect("Executing insert statement " + insert_line)
    child.expect(REPL_PROMPT)
    select_line = "select"
    child.sendline(select_line)
    child.expect("Executing select statement " + select_line)
    expected_row = repr(TableRowDef(1, "aaa", "bbb")).replace('(', '\\(').replace(')', '\\)')
    child.expect(expected_row)
    child.expect(REPL_PROMPT)


def test_select(child):
    select_line = "select"
    child.sendline(select_line)
    child.expect("Executing select statement " + select_line)
    child.expect(REPL_PROMPT)
