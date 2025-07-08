from typing import Any

from muffinscript.constants import SUPPORTED_TYPES


class BaseNode:
    """All nodes share this base node."""

    def __init__(self, line_number: int, value: SUPPORTED_TYPES = None):
        self.line_number = line_number
        self.value = value


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
        self.left = left
        self.right = right


class IfNode(BaseNode):
    """If statement: if (foo == bar) { ... }"""

    def __init__(self, condition: Any, body: list[Any], line_number: int):
        super().__init__(line_number)
        self.condition = condition
        self.body = body
