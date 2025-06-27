from muffinscript.ast import (
    BoolNode,
    FloatNode,
    IntNode,
    NullNode,
    StringNode,
)


def test_string_node():
    node = StringNode(value="hello world", line_number=1)
    assert node.value == "hello world"
    assert node.line_number == 1


def test_int_node():
    node = IntNode(value=2, line_number=1)
    assert node.value == 2
    assert node.line_number == 1


def test_float_node():
    node = FloatNode(value=2.5, line_number=1)
    assert node.value == 2.5
    assert node.line_number == 1


def test_bool_node():
    node = BoolNode(value=True, line_number=1)
    assert node.value is True
    assert node.line_number == 1


def test_null_node():
    node = NullNode(value=None, line_number=1)
    assert node.value is None
    assert node.line_number == 1
