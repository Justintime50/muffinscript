import operator
import os


# Env Vars
MUFFIN_DEBUG = os.getenv("MUFFIN_DEBUG")

# Supported constants
SUPPORTED_TYPES = str | int | float | bool | list | None
SUPPORTED_STATEMENTS = set(
    [
        "cat",
        "else",
        "if",
        "p",
        "sleep",
        "type",
    ]
)
SUPPORTED_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

# Mappings
PYTHON_TO_MUFFIN_TYPES = {
    str: "str",
    int: "int",
    float: "float",
    bool: "bool",
    list: "list",
    type(None): "null",
}

# Error messages
INVALID_COERCION = "Invalid coercion, could not convert to type"
INVALID_CONCATENATION = "Invalid concatenation, only strings allowed"
INVALID_EXPRESSION = "Invalid expression"
INVALID_FLOAT = "Invalid float"
UNDEFINED_VARIABLE = "Undefined variable"
UNSUPPORTED_STATEMENT = "Unsupported statement"
UNTERMINATED_STRINGS = "Unterminated string"

RESERVED_KEYWORDS = set(SUPPORTED_STATEMENTS) | set(PYTHON_TO_MUFFIN_TYPES.values())
