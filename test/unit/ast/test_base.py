from muffinscript.ast import (
    ArithmeticNode,
    AssignNode,
    BaseNode,
)
from muffinscript.ast.base import IfNode


def test_base_node():
    node = BaseNode(line_number=1)
    assert node.line_number == 1


def test_assign_node():
    node = AssignNode(var_name="foo", expression="2 + 2", line_number=1)
    assert node.var_name == "foo"
    assert node.expression == "2 + 2"
    assert node.line_number == 1


def test_arithmetic_node():
    node = ArithmeticNode(operator="+", left=2, right=3, line_number=1)
    assert node.operator == "+"
    assert node.left == 2
    assert node.right == 3
    assert node.line_number == 1


def test_if_node():
    node = IfNode(condition="foo == bar", body=["p", "(", "true", ")"], line_number=1)
    assert node.condition == "foo == bar"
    assert node.body == ["p", "(", "true", ")"]
    assert node.line_number == 1
