from muffinscript.ast import (
    CatNode,
    PrintNode,
    SleepNode,
)
from muffinscript.ast.standard_lib import (
    FloatCoerceNode,
    IntCoerceNode,
    StringCoerceNode,
    TypeCheckNode,
)


def test_print_node():
    node = PrintNode(value="hello world", line_number=1)
    assert node.value == "hello world"
    assert node.line_number == 1


def test_cat_node():
    node = CatNode(args=["hello", "world"], line_number=1)
    assert node.args == ["hello", "world"]
    assert node.line_number == 1


def test_sleep_node():
    node = SleepNode(duration=1000.5, line_number=1)
    assert node.duration == 1000.5
    assert node.line_number == 1


def test_string_coerce_node():
    node = StringCoerceNode(value="hello world", line_number=1)
    assert node.value == "hello world"
    assert node.line_number == 1


def test_int_coerce_node():
    node = IntCoerceNode(value=2, line_number=1)
    assert node.value == 2
    assert node.line_number == 1


def test_float_coerce_node():
    node = FloatCoerceNode(value=2.5, line_number=1)
    assert node.value == 2.5
    assert node.line_number == 1


def test_type_check_node():
    node = TypeCheckNode(value="hello", line_number=1)
    assert node.value == "hello"
    assert node.line_number == 1
