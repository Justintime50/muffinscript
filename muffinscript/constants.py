import operator


# Supported types
SUPPORTED_TYPES = str | int | float | bool | None
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
PYTHON_TO_MUFFIN_TYPES = {
    str: "str",
    int: "int",
    float: "float",
    bool: "bool",
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
