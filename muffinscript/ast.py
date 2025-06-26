from typing import Literal

from muffinscript.constants import (
    SUPPORTED_OPERATORS,
    SUPPORTED_TYPES,
)


class BaseNode:
    """All nodes share this base node."""

    def __init__(self, line_number: int):
        self.line_number = line_number


class StringNode(BaseNode):
    """Strings: 'hello world'"""

    def __init__(self, value: str, line_number: int):
        super().__init__(line_number)
        self.value = value


class IntNode(BaseNode):
    """Integers: 42"""

    def __init__(self, value: int, line_number: int):
        super().__init__(line_number)
        self.value = value


class FloatNode(BaseNode):
    """Floats: 42.3"""

    def __init__(self, value: float, line_number: int):
        super().__init__(line_number)
        self.value = value


class BoolNode(BaseNode):
    """Booleans: true"""

    def __init__(self, value: bool, line_number: int):
        super().__init__(line_number)
        self.value = value


class NullNode(BaseNode):
    """Null: null"""

    def __init__(self, value: None, line_number: int):
        super().__init__(line_number)
        self.value = value


class PrintNode(BaseNode):
    """Print function: p(foo)"""

    def __init__(self, value: BaseNode, line_number: int):
        super().__init__(line_number)
        self.value = value


class AssignNode(BaseNode):
    """Variable assignment: foo = 'hello world'"""

    def __init__(self, var_name: str, expression: BaseNode, line_number: int):
        super().__init__(line_number)
        self.var_name = var_name
        self.expression = expression


class ArithmeticNode(BaseNode):
    """Arithmetic expressions: 2 + 2"""

    def __init__(
        self,
        operator: Literal[SUPPORTED_OPERATORS.keys()],
        left: BaseNode,
        right: BaseNode,
        line_number: int,
    ):
        super().__init__(line_number)
        self.operator = operator
        self.left = left
        self.right = right


class CatNode(BaseNode):
    """Cat function: cat("hello ", "world")"""

    def __init__(self, args: list[SUPPORTED_TYPES], line_number: int):
        super().__init__(line_number)
        self.args = args
