from typing import Any

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
    StringNode,
)
from muffinscript.constants import (
    SUPPORTED_OPERATORS,
    SUPPORTED_TYPES,
    UNDEFINED_VARIABLE,
    UNSUPPORTED_STATEMENT,
)
from muffinscript.errors import MuffinScriptSyntaxError


def parse_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> Any:
    """Parses tokens before sending them to the interpreter to ensure they have no syntax errors."""
    # Print
    if "p" in tokens:
        return _parse_print_tokens(tokens, line_number)
    # Variable assignment
    elif "=" in tokens:
        return _parse_variable_tokens(tokens, line_number)
    else:
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)


def _parse_print_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> PrintNode:
    """Token schema: ["p", "(", "foo", ")"]"""
    if tokens[0] != "p" or len(tokens) < 4 or tokens[1] != "(" or tokens[-1] != ")":
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
    if len(tokens) == 4 and isinstance(tokens[2], str):
        # Using a variable
        expression: Any = tokens[2]
    else:
        # Using an expression
        expression = _parse_expression(tokens[2:-1], line_number)
    return PrintNode(expression, line_number)


def _parse_variable_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> AssignNode:
    """Token schema: ["foo", "=", "hello world"]"""
    expression: Any = None
    if len(tokens) < 3:
        raise MuffinScriptSyntaxError(UNDEFINED_VARIABLE, line_number)
    expression = _parse_expression(tokens[2:], line_number)
    if expression is None:
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
    return AssignNode(
        var_name=str(tokens[0]),
        expression=expression,
        line_number=line_number,
    )


def _parse_expression(tokens: list[SUPPORTED_TYPES], line_number: int) -> BaseNode | None:
    """Parses an expression from provided tokens."""
    if tokens[0] == "cat":
        if len(tokens) < 4 or tokens[1] != "(" or tokens[-1] != ")":
            raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
        return CatNode(
            args=[_parse_expression([token], line_number) for token in tokens[2:-1]], line_number=line_number
        )
    elif len(tokens) == 3 and tokens[1] in SUPPORTED_OPERATORS.keys():
        # TODO: Support multiple arithmetic chaining
        return ArithmeticNode(
            operator=str(tokens[1]),
            left=tokens[0],
            right=tokens[2],
            line_number=line_number,
        )
    elif len(tokens) == 1 and isinstance(tokens[0], str):
        # Strip quotes if it's a string literal
        if tokens[0].startswith('"') and tokens[0].endswith('"'):
            return StringNode(tokens[0][1:-1], line_number)
        return StringNode(tokens[0], line_number)
    elif len(tokens) == 1 and (tokens[0] is True or tokens[0] is False):
        return BoolNode(str(tokens[0]).lower(), line_number)
    elif len(tokens) == 1 and tokens[0] is None:
        return NullNode("null", line_number)
    elif len(tokens) == 1 and isinstance(tokens[0], int):
        return IntNode(tokens[0], line_number)
    elif len(tokens) == 1 and isinstance(tokens[0], float):
        return FloatNode(tokens[0], line_number)

    return None
