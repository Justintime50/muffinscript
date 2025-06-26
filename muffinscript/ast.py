class BaseNode:
    """All nodes share this base node."""

    def __init__(self, line_number):
        self.line_number = line_number


class StringNode(BaseNode):
    """Strings: 'hello world'"""

    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value


class IntNode(BaseNode):
    """Integers: 42"""

    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value


class FloatNode(BaseNode):
    """Floats: 42.3"""

    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value


class BoolNode(BaseNode):
    """Booleans: true"""

    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value


class NullNode(BaseNode):
    """Null: null"""

    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value


class PrintNode(BaseNode):
    """Print function: p(foo)"""

    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value


class AssignNode(BaseNode):
    """Variable assignment: foo = 'hello world'"""

    def __init__(self, var_name, expression, line_number):
        super().__init__(line_number)
        self.var_name = var_name
        self.expression = expression


class ArithmeticNode(BaseNode):
    """Arithmetic expressions: 2 + 2"""

    def __init__(self, operator, left, right, line_number):
        super().__init__(line_number)
        self.operator = operator
        self.left = left
        self.right = right


class CatNode(BaseNode):
    """Cat function: cat("hello ", "world")"""

    def __init__(self, args, line_number):
        super().__init__(line_number)
        self.args = args
