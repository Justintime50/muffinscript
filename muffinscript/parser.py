from typing import Any

from muffinscript.ast import (
    ArithmeticNode,
    AssignNode,
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
    UNSUPPORTED_STATEMENT,
)
from muffinscript.errors import MuffinScriptSyntaxError


def parse_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> Any:
    """Parses tokens before sending them to the interpreter to ensure they have no syntax errors."""
    # Print
    if len(tokens) > 1 and tokens[0] == "p":
        return _parse_print_tokens(tokens, line_number)
    # Variable assignment
    elif len(tokens) > 1 and tokens[1] == "=":
        return _parse_variable_tokens(tokens, line_number)
    else:
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)


def _parse_print_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> PrintNode:
    """Print tokens should look like: ["p", "(", "foo", ")"]"""
    if len(tokens) != 4 or tokens[1] != "(" or tokens[3] != ")":
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
    return PrintNode(tokens[2], line_number)


def _parse_variable_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> AssignNode:
    """Variable tokens should look like: ["foo", "=", "hello world"]"""
    expression = _parse_expression(tokens[2:], line_number)
    return AssignNode(
        var_name=tokens[0],
        expression=expression,
        line_number=line_number,
    )


def _parse_expression(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> StringNode | BoolNode | NullNode | IntNode | FloatNode | ArithmeticNode | CatNode:
    """Parse the expression of a variable before assignment."""
    # eg: single value, direct assignment
    if len(tokens) == 1:
        token = tokens[0]

        if isinstance(token, str) and token.startswith('"') and token.endswith('"'):
            return StringNode(token, line_number)
        elif token is True or token is False:
            return BoolNode(token, line_number)
        elif token is None:
            return NullNode(token, line_number)
        elif isinstance(token, int):
            return IntNode(token, line_number)
        elif isinstance(token, float):
            return FloatNode(token, line_number)

    # Concatenation
    elif len(tokens) > 1 and tokens[0] == "cat":
        return _parse_concatenate_tokens(tokens, line_number)

    # eg: expression such as `2 + 2`, `3 * 4`, etc
    # TODO: Support multiple arithmetic chaining
    elif len(tokens) == 3 and tokens[1] in SUPPORTED_OPERATORS.keys():
        return ArithmeticNode(
            operator=str(tokens[1]),
            left=tokens[0],
            right=tokens[2],
            line_number=line_number,
        )

    # eg: missing assignment
    raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)


def _parse_concatenate_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> CatNode:
    """Parse concatenating strings together"""
    if len(tokens) < 4 or tokens[1] != "(" or tokens[-1] != ")":
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
    return CatNode(args=tokens[2:-1], line_number=line_number)
