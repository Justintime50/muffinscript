from .base import BaseNode


class BoolNode(BaseNode):
    """Booleans: true"""

    def __init__(self, value: str, line_number: int):
        super().__init__(line_number, value)


class FloatNode(BaseNode):
    """Floats: 42.3"""

    def __init__(self, value: float, line_number: int):
        super().__init__(line_number, value)


class IntNode(BaseNode):
    """Integers: 42"""

    def __init__(self, value: int, line_number: int):
        super().__init__(line_number, value)


class StringNode(BaseNode):
    """Strings: 'hello world'"""

    def __init__(self, value: str, line_number: int):
        super().__init__(line_number, value)


class NullNode(BaseNode):
    """Null: null"""

    def __init__(self, value: str, line_number: int):
        super().__init__(line_number, value)
