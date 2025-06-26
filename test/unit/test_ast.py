from muffinscript.ast import (
    ArithmeticNode,
    AssignNode,
    BaseNode,
    BoolNode,
    CatNode,
    FloatNode,
    IntNode,
    NullNode,
    PrintNode,
    SleepNode,
    StringNode,
)


def test_base_node():
    node = BaseNode(line_number=1)
    assert node.line_number == 1


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


def test_print_node():
    node = PrintNode(value="hello world", line_number=1)
    assert node.value == "hello world"
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


def test_cat_node():
    node = CatNode(args=["hello", "world"], line_number=1)
    assert node.args == ["hello", "world"]
    assert node.line_number == 1


def test_sleep_node():
    node = SleepNode(duration=1000.5, line_number=1)
    assert node.duration == 1000.5
    assert node.line_number == 1
