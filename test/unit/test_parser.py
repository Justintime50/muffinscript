import pytest

from muffinscript.errors import (
    MuffinScriptRuntimeError,
    MuffinScriptSyntaxError,
)
from muffinscript.parser import parse_tokens


def test_parse_print_tokens():
    """Test that we parse the `p()` function correctly."""
    node = parse_tokens(["p", "(", "foo", ")"], 1)
    assert node.value == "foo"
    assert node.line_number == 1

    node = parse_tokens(["p", "(", 2, "+", 3, ")"], 2)
    assert node.value.operator == "+"
    assert node.value.left == 2
    assert node.value.right == 3
    assert node.line_number == 2

    node = parse_tokens(["p", "(", True, ")"], 3)
    assert node.value.value == "true"
    assert node.line_number == 3

    node = parse_tokens(["p", "(", None, ")"], 4)
    assert node.value.value == "null"
    assert node.line_number == 4

    node = parse_tokens(["p", "(", 2, ")"], 5)
    assert node.value.value == 2
    assert node.line_number == 5

    node = parse_tokens(["p", "(", 2.5, ")"], 6)
    assert node.value.value == 2.5
    assert node.line_number == 6

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["p", "(", "foo"], 7)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 7"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["foo", "=", "cat", "(", "foo"], 8)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 8"


def test_parse_variable_tokens():
    """Test that we parse variables."""
    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["foo", "="], 0)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Undefined variable | line: 0"

    node = parse_tokens(["foo", "=", '"hello world"'], 1)
    assert node.var_name == "foo"
    assert node.expression.value == "hello world"
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

    node = parse_tokens(["foo", "=", "cat", "(", "hello ", "bar", ")"], 13)
    assert node.var_name == "foo"
    assert node.expression.args[0].value == "hello "
    assert node.expression.args[1].value == "bar"
    assert node.line_number == 13

    node = parse_tokens(["sleep", "(", 1000.5, ")"], 14)
    assert node.duration == 1000.5
    assert node.line_number == 14

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["foo", "=", "2", "?", "2"], 15)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 15"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["sleep", "(", None, ")"], 16)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Invalid float | line: 16"

    node = parse_tokens(["foo", "=", "str", "(", 2, ")"], 17)
    assert node.expression.value == "2"
    assert node.line_number == 17

    node = parse_tokens(["foo", "=", "int", "(", "2", ")"], 18)
    assert node.expression.value == 2
    assert node.line_number == 18

    with pytest.raises(MuffinScriptRuntimeError) as error:
        parse_tokens(["foo", "=", "int", "(", "hello", ")"], 19)
    assert str(error.value) == "\033[31mRUNTIME ERROR\033[0m - Invalid coercion, could not convert to type | line: 19"

    node = parse_tokens(["foo", "=", "float", "(", 2, ")"], 20)
    assert node.expression.value == 2.0
    assert node.line_number == 20

    with pytest.raises(MuffinScriptRuntimeError) as error:
        parse_tokens(["foo", "=", "float", "(", "hello", ")"], 21)
    assert str(error.value) == "\033[31mRUNTIME ERROR\033[0m - Invalid coercion, could not convert to type | line: 21"

    node = parse_tokens(["foo", "=", "type", "(", 2, ")"], 21)
    assert node.expression.value.value == 2
    assert node.line_number == 21

    node = parse_tokens(["if", "(", "foo", "==", "bar", ")", "{", "p", "(", "true", ")", "}"], 22)
    assert node.condition.operator == "=="
    assert node.condition.left == "foo"
    assert node.condition.right == "bar"
    assert node.body[0].value == "true"
    assert node.line_number == 22
