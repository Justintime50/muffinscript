import operator


# Supported types
SUPPORTED_TYPES = str | int | float | bool | None
SUPPORTED_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

# Error messages
INVALID_EXPRESSION = "Invalid expression"
INVALID_FLOAT = "Invalid float"
UNDEFINED_VARIABLE = "Undefined variable: {}"
UNSUPPORTED_STATEMENT = "Unsupported statement"
UNTERMINATED_STRINGS = "Unterminated string"
