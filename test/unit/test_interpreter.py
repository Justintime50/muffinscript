from unittest.mock import patch

import pytest

from muffinscript.ast.base import (
    ArithmeticNode,
    AssignNode,
    ForLoopNode,
    IfNode,
)
from muffinscript.ast.standard_lib import (
    CatNode,
    PrintNode,
    SleepNode,
    TypeCheckNode,
)
from muffinscript.ast.types import (
    BoolNode,
    FloatNode,
    IntNode,
    ListNode,
    NullNode,
    StringNode,
)
from muffinscript.errors import (
    MuffinScriptRuntimeError,
)
from muffinscript.interpreter import evaluate


def test_evaluate_prints(capsys):
    node = PrintNode("foo", 1)

    evaluate(node, {"foo": "hello world"}, node.line_number)
    captured = capsys.readouterr()
    assert captured.out.strip() == "hello world"

    evaluate(node, {"foo": "true"}, node.line_number)
    captured = capsys.readouterr()
    assert captured.out.strip() == "true"

    evaluate(node, {"foo": "false"}, node.line_number)
    captured = capsys.readouterr()
    assert captured.out.strip() == "false"

    evaluate(node, {"foo": "null"}, node.line_number)
    captured = capsys.readouterr()
    assert captured.out.strip() == "null"

    evaluate(node, {"foo": 2}, node.line_number)
    captured = capsys.readouterr()
    assert captured.out.strip() == "2"

    evaluate(node, {"foo": 2.5}, node.line_number)
    captured = capsys.readouterr()
    assert captured.out.strip() == "2.5"

    evaluate(node, {"foo": [1, 2, 3]}, node.line_number)
    captured = capsys.readouterr()
    assert captured.out.strip() == "[1, 2, 3]"


def test_evaluate_variable_assignment():
    node = AssignNode("foo", StringNode("hello world", 1), 1)

    expression = evaluate(node, {}, node.line_number)
    assert expression == "hello world"


def test_evaluate_string_node():
    node = StringNode("hello world", 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == "hello world"

    node = StringNode("hello #{foo}", 2)
    expression = evaluate(node, {"foo": "world"}, node.line_number)
    assert expression == "hello world"

    node = StringNode("hello #{bar}", 3)
    with pytest.raises(MuffinScriptRuntimeError) as error:
        evaluate(node, {"foo": "world"}, node.line_number)
    assert str(error.value) == "\033[31mRUNTIME ERROR\033[0m - Undefined variable | line: 3"


def test_evaluate_int_node():
    node = IntNode(2, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == 2


def test_evaluate_float_node():
    node = FloatNode(2.5, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == 2.5


def test_evaluate_bool_node():
    node = BoolNode(True, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression is True

    node = BoolNode(False, 2)
    expression = evaluate(node, {}, node.line_number)
    assert expression is False


def test_evaluate_null_node():
    node = NullNode(None, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression is None


def test_evaluate_list_node():
    node = ListNode([IntNode(1, 1), IntNode(2, 1), IntNode(3, 1)], 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == [1, 2, 3]

    node = ListNode([StringNode("hello", 2), StringNode("world", 2)], 2)
    expression = evaluate(node, {}, node.line_number)
    assert expression == ["hello", "world"]


def test_evaluate_for_loop_node():
    node = ForLoopNode("item", [IntNode(1, 1), IntNode(2, 1), IntNode(3, 1)], [PrintNode("item", 1)], 1)
    expression = evaluate(node, {}, node.line_number)
    assert all(isinstance(item, PrintNode) for item in expression)

    node = ForLoopNode("item", "foo", [PrintNode("item", 1)], 2)
    expression = evaluate(
        node,
        {"foo": [IntNode(1, node.line_number), IntNode(2, node.line_number), IntNode(3, node.line_number)]},
        node.line_number,
    )
    assert all(isinstance(item, PrintNode) for item in expression)

    node = ForLoopNode("item", 1, [PrintNode("item", 1)], 3)
    with pytest.raises(MuffinScriptRuntimeError) as error:
        evaluate(node, {"foo": "world"}, node.line_number)
    assert str(error.value) == "\033[31mRUNTIME ERROR\033[0m - Unsupported statement | line: 3"


def test_evaluate_arithmetic_node():
    node = ArithmeticNode("+", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == 5

    node = ArithmeticNode("-", 2, 3, 2)
    expression = evaluate(node, {}, node.line_number)
    assert expression == -1

    node = ArithmeticNode("*", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == 6

    node = ArithmeticNode("/", 2, 2, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == 1

    node = ArithmeticNode("%", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == 2

    node = ArithmeticNode("<", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression is True

    node = ArithmeticNode(">", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression is False

    node = ArithmeticNode("<=", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression is True

    node = ArithmeticNode(">=", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression is False

    node = ArithmeticNode("==", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression is False

    node = ArithmeticNode("!=", 2, 3, 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression is True


def test_evaluate_cat_node():
    node = CatNode([StringNode("hello ", 1), StringNode("foo", 1)], 1)
    expression = evaluate(node, {"foo": "world"}, node.line_number)
    assert expression == "hello world"


def test_evaluate_sleep_node():
    node = SleepNode(2, 1)
    with patch("time.sleep") as mock_sleep:
        evaluate(node, {}, node.line_number)
        mock_sleep.assert_called_once_with(2)


def test_evaluate_type_check_node():
    node = TypeCheckNode(StringNode("hello", 1), 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression == "str"

    node = TypeCheckNode(IntNode(2, 2), 2)
    expression = evaluate(node, {}, node.line_number)
    assert expression == "int"

    node = TypeCheckNode(FloatNode(2.5, 3), 3)
    expression = evaluate(node, {}, node.line_number)
    assert expression == "float"

    node = TypeCheckNode(BoolNode(True, 4), 4)
    expression = evaluate(node, {}, node.line_number)
    assert expression == "bool"

    node = TypeCheckNode(NullNode(None, 5), 5)
    expression = evaluate(node, {}, node.line_number)
    assert expression == "null"

    node = TypeCheckNode(ListNode([StringNode("hello", 6)], 6), 6)
    expression = evaluate(node, {}, node.line_number)
    assert expression == "list"


def test_evaluate_if_node():
    node = IfNode(ArithmeticNode("==", 2, 2, 1), [PrintNode(True, 1)], 1)
    expression = evaluate(node, {}, node.line_number)
    assert expression[0].value is True

    node = IfNode(ArithmeticNode("==", 2, 3, 1), [PrintNode(True, 1)], 1, [PrintNode(False, 1)])
    expression = evaluate(node, {}, node.line_number)
    assert expression[0].value is False


def test_evaluate_undefined_variable():
    node = "foo"
    with pytest.raises(MuffinScriptRuntimeError) as error:
        evaluate(node, {}, 1)
    assert str(error.value) == "\033[31mRUNTIME ERROR\033[0m - Undefined variable | line: 1"
