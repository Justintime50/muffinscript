from typing import Any

from muffinscript.constants import SUPPORTED_TYPES


class BaseNode:
    """All nodes share this base node."""

    def __init__(self, line_number: int, value: SUPPORTED_TYPES = None):
        self.line_number = line_number
        self.value = value


class StringNode(BaseNode):
    """Strings: 'hello world'"""

    def __init__(self, value: str, line_number: int):
        super().__init__(line_number, value)


class IntNode(BaseNode):
    """Integers: 42"""

    def __init__(self, value: int, line_number: int):
        super().__init__(line_number, value)


class FloatNode(BaseNode):
    """Floats: 42.3"""

    def __init__(self, value: float, line_number: int):
        super().__init__(line_number, value)


class BoolNode(BaseNode):
    """Booleans: true"""

    def __init__(self, value: str, line_number: int):
        super().__init__(line_number, value)


class NullNode(BaseNode):
    """Null: null"""

    def __init__(self, value: str, line_number: int):
        super().__init__(line_number, value)


class PrintNode(BaseNode):
    """Print function: p(foo)"""

    def __init__(self, value: Any, line_number: int):
        super().__init__(line_number, value)


class AssignNode(BaseNode):
    """Variable assignment: foo = 'hello world'"""

    def __init__(self, var_name: str, expression: Any, line_number: int):
        super().__init__(line_number)
        self.var_name = var_name
        self.expression = expression


class ArithmeticNode(BaseNode):
    """Arithmetic expressions: 2 + 2"""

    def __init__(
        self,
        operator: str,  # We checked this against SUPPORTED_OPERATORS elsewhere
        left: Any,
        right: Any,
        line_number: int,
    ):
        super().__init__(line_number)
        self.operator = operator
        self.left = left
        self.right = right


class CatNode(BaseNode):
    """Cat function: cat("hello ", "world")"""

    def __init__(self, args: list[Any], line_number: int):
        super().__init__(line_number)
        self.args = args


class SleepNode(BaseNode):
    """Sleep function: sleep(1000)"""

    def __init__(self, duration: Any, line_number: int):
        super().__init__(line_number, duration)
        self.duration = duration
