import pytest

from muffinscript.errors import MuffinScriptSyntaxError
from muffinscript.parser import parse_tokens


def test_tokens_unknown_statement():
    """Test we throw an error when an unknown statement is used."""
    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["?"], 1)
    assert str(error.value) == "\033[31mERROR\033[0m - Unsupported statement | line: 1"


def test_parse_print_tokens():
    """Test that we parse the `p()` function correctly."""
    node = parse_tokens(["p", "(", "foo", ")"], 1)
    assert node.value == "foo"
    assert node.line_number == 1

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["p", "(", "foo"], 2)
    assert str(error.value) == "\033[31mERROR\033[0m - Unsupported statement | line: 2"


def test_parse_variable_tokens():
    """Test that we parse variables."""
    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["foo", "="], 0)
    assert str(error.value) == "\033[31mERROR\033[0m - Undefined variable | line: 0"

    node = parse_tokens(["foo", "=", '"hello world"'], 1)
    assert node.var_name == "foo"
    assert node.expression.value == '"hello world"'
    assert node.line_number == 1

    node = parse_tokens(["foo", "=", 2, "+", 2], 2)
    assert node.var_name == "foo"
    assert node.expression.operator == "+"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 2

    node = parse_tokens(["foo", "=", 2, "-", 2], 3)
    assert node.var_name == "foo"
    assert node.expression.operator == "-"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 3

    node = parse_tokens(["foo", "=", 2, "*", 2], 4)
    assert node.var_name == "foo"
    assert node.expression.operator == "*"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 4

    node = parse_tokens(["foo", "=", 2, "/", 2], 5)
    assert node.var_name == "foo"
    assert node.expression.operator == "/"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 5

    node = parse_tokens(["foo", "=", 2, "%", 2], 6)
    assert node.var_name == "foo"
    assert node.expression.operator == "%"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 6

    node = parse_tokens(["foo", "=", 2, "==", 2], 7)
    assert node.var_name == "foo"
    assert node.expression.operator == "=="
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 7

    node = parse_tokens(["foo", "=", 2, "!=", 2], 8)
    assert node.var_name == "foo"
    assert node.expression.operator == "!="
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 8

    node = parse_tokens(["foo", "=", 2, ">", 2], 9)
    assert node.var_name == "foo"
    assert node.expression.operator == ">"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 9

    node = parse_tokens(["foo", "=", 2, ">=", 2], 10)
    assert node.var_name == "foo"
    assert node.expression.operator == ">="
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 10

    node = parse_tokens(["foo", "=", 2, "<", 2], 11)
    assert node.var_name == "foo"
    assert node.expression.operator == "<"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 11

    node = parse_tokens(["foo", "=", 2, "<=", 2], 12)
    assert node.var_name == "foo"
    assert node.expression.operator == "<="
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 12

    # with pytest.raises(MuffinScriptSyntaxError) as error:
    #     parse_tokens(["foo", "=", "2", "?", "2"], 1)
    # assert str(error.value) == "\033[31mERROR\033[0m - Unsupported statement | line: 1"
