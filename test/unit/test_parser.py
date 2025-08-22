import pytest

from muffinscript.ast.standard_lib import PrintNode
from muffinscript.ast.types import IntNode
from muffinscript.errors import (
    MuffinScriptRuntimeError,
    MuffinScriptSyntaxError,
)
from muffinscript.parser import parse_tokens


def test_parse_print_tokens():
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


def test_parse_variable_tokens():
    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["foo", "="], 0)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Undefined variable | line: 0"

    node = parse_tokens(["foo", "=", '"hello world"'], 1)
    assert node.var_name == "foo"
    assert node.expression.value == "hello world"
    assert node.line_number == 1

    node = parse_tokens(["foo", "=", 2], 2)
    assert node.var_name == "foo"
    assert node.expression.value == 2
    assert node.line_number == 2

    node = parse_tokens(["foo", "=", 2.5], 3)
    assert node.var_name == "foo"
    assert node.expression.value == 2.5
    assert node.line_number == 3

    node = parse_tokens(["foo", "=", 2, "+", 2], 4)
    assert node.var_name == "foo"
    assert node.expression.operator == "+"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 4

    node = parse_tokens(["foo", "=", 2, "-", 2], 5)
    assert node.var_name == "foo"
    assert node.expression.operator == "-"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 5

    node = parse_tokens(["foo", "=", 2, "*", 2], 6)
    assert node.var_name == "foo"
    assert node.expression.operator == "*"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 6

    node = parse_tokens(["foo", "=", 2, "/", 2], 7)
    assert node.var_name == "foo"
    assert node.expression.operator == "/"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 7

    node = parse_tokens(["foo", "=", 2, "%", 2], 8)
    assert node.var_name == "foo"
    assert node.expression.operator == "%"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 8

    node = parse_tokens(["foo", "=", 2, "==", 2], 9)
    assert node.var_name == "foo"
    assert node.expression.operator == "=="
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 9

    node = parse_tokens(["foo", "=", 2, "!=", 2], 10)
    assert node.var_name == "foo"
    assert node.expression.operator == "!="
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 10

    node = parse_tokens(["foo", "=", 2, ">", 2], 11)
    assert node.var_name == "foo"
    assert node.expression.operator == ">"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 11

    node = parse_tokens(["foo", "=", 2, ">=", 2], 12)
    assert node.var_name == "foo"
    assert node.expression.operator == ">="
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 12

    node = parse_tokens(["foo", "=", 2, "<", 2], 13)
    assert node.var_name == "foo"
    assert node.expression.operator == "<"
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 13

    node = parse_tokens(["foo", "=", 2, "<=", 2], 14)
    assert node.var_name == "foo"
    assert node.expression.operator == "<="
    assert node.expression.left == 2
    assert node.expression.right == 2
    assert node.line_number == 14

    node = parse_tokens(["foo", "=", "cat", "(", "hello ", "bar", ")"], 15)
    assert node.var_name == "foo"
    assert node.expression.args[0].value == "hello "
    assert node.expression.args[1].value == "bar"
    assert node.line_number == 15

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["foo", "=", "cat", "(", "foo"], 16)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 16"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["foo", "=", "2", "?", "2"], 17)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 17"

    node = parse_tokens(["foo", "=", "str", "(", 2, ")"], 18)
    assert node.expression.value == "2"
    assert node.line_number == 18

    node = parse_tokens(["foo", "=", "int", "(", "2", ")"], 19)
    assert node.expression.value == 2
    assert node.line_number == 19

    with pytest.raises(MuffinScriptRuntimeError) as error:
        parse_tokens(["foo", "=", "int", "(", "hello", ")"], 20)
    assert str(error.value) == "\033[31mRUNTIME ERROR\033[0m - Invalid coercion, could not convert to type | line: 20"

    node = parse_tokens(["foo", "=", "float", "(", 2, ")"], 21)
    assert node.expression.value == 2.0
    assert node.line_number == 21

    with pytest.raises(MuffinScriptRuntimeError) as error:
        parse_tokens(["foo", "=", "float", "(", "hello", ")"], 22)
    assert str(error.value) == "\033[31mRUNTIME ERROR\033[0m - Invalid coercion, could not convert to type | line: 22"

    node = parse_tokens(["foo", "=", "type", "(", 2, ")"], 23)
    assert node.expression.value.value == 2
    assert node.line_number == 23

    node = parse_tokens(["foo", "=", "type", "(", "foo", ")"], 24)
    assert node.expression.value == "foo"
    assert node.line_number == 24


def test_parse_sleep_tokens():
    node = parse_tokens(["sleep", "(", 10.5, ")"], 1)
    assert node.duration == 10.5
    assert node.line_number == 1

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["sleep", "(", None, ")"], 16)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Invalid float | line: 16"


def test_parse_if_tokens():
    # If with no else
    node = parse_tokens(["if", "(", "foo", "==", "bar", ")", "{", "p", "(", "true", ")", "}"], 1)
    assert node.condition.operator == "=="
    assert node.condition.left == "foo"
    assert node.condition.right == "bar"
    assert node.body[0].value == "true"
    assert node.line_number == 1

    # If with else
    node = parse_tokens(
        ["if", "(", "foo", "==", "bar", ")", "{", "p", "(", "true", ")", "}", "else", "{", "p", "(", "false", ")", "}"],
        2,
    )
    assert node.condition.operator == "=="
    assert node.condition.left == "foo"
    assert node.condition.right == "bar"
    assert node.body[0].value == "true"
    assert node.else_body[0].value == "false"
    assert node.line_number == 2

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["if", "(", "2 == 2"], 3)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 3"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["if", "(", "2 == 2", ")", "{"], 4)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 4"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["if", "(", "2 == 2", ")", "{", "p", "(", "true", ")", "}", "else", "{"], 5)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 5"


def test_parse_for_loop_tokens():
    node = parse_tokens(["for", "(", "item", "in", "myList", ")", "{", "p", "(", "item", ")", "}"], 1)
    assert node.item_name == "item"
    assert node.iterable == "myList"
    assert isinstance(node.body[0], PrintNode)
    assert node.line_number == 1

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["for", "(", "item", "myList", ")", "{", "p", "(", "item", ")", "}"], 2)  # no "in"
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 2"


def test_parse_expressions():
    node = parse_tokens(["cat", "(", "hello", "world", ")"], 1)
    assert node.args[0].value == "hello"
    assert node.args[1].value == "world"
    assert node.line_number == 1

    node = parse_tokens(["str", "(", 2, ")"], 2)
    assert node.value == "2"
    assert node.line_number == 2

    node = parse_tokens(["int", "(", "2", ")"], 3)
    assert node.value == 2
    assert node.line_number == 3

    node = parse_tokens(["float", "(", "2.5", ")"], 4)
    assert node.value == 2.5
    assert node.line_number == 4

    node = parse_tokens(["type", "(", 2, ")"], 5)
    assert isinstance(node.value, IntNode)
    assert node.line_number == 5

    node = parse_tokens([2, "+", 2], 6)
    assert node.operator == "+"
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 6

    node = parse_tokens([2, "-", 2], 7)
    assert node.operator == "-"
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 7

    node = parse_tokens([2, "*", 2], 8)
    assert node.operator == "*"
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 8

    node = parse_tokens([2, "/", 2], 9)
    assert node.operator == "/"
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 9

    node = parse_tokens([2, "%", 2], 10)
    assert node.operator == "%"
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 10

    node = parse_tokens([2, "==", 2], 11)
    assert node.operator == "=="
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 11

    node = parse_tokens([2, "!=", 2], 12)
    assert node.operator == "!="
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 12

    node = parse_tokens([2, ">", 2], 13)
    assert node.operator == ">"
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 13

    node = parse_tokens([2, ">=", 2], 14)
    assert node.operator == ">="
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 14

    node = parse_tokens([2, "<", 2], 15)
    assert node.operator == "<"
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 15

    node = parse_tokens([2, "<=", 2], 16)
    assert node.operator == "<="
    assert node.left == 2
    assert node.right == 2
    assert node.line_number == 16

    node = parse_tokens(['"hello world"'], 17)
    assert node.value == "hello world"
    assert node.line_number == 17

    node = parse_tokens([2], 18)
    assert node.value == 2
    assert node.line_number == 18

    node = parse_tokens([2.5], 18)
    assert node.value == 2.5
    assert node.line_number == 18

    node = parse_tokens([True], 19)
    assert node.value == "true"
    assert node.line_number == 19

    node = parse_tokens([False], 20)
    assert node.value == "false"
    assert node.line_number == 20

    node = parse_tokens([None], 21)
    assert node.value == "null"
    assert node.line_number == 21
