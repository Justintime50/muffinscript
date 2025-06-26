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
    if tokens[0] != "p" or len(tokens) != 4 or tokens[1] != "(" or tokens[3] != ")":
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
    return PrintNode(tokens[2], line_number)


def _parse_variable_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> AssignNode:
    """Token schema: ["foo", "=", "hello world"]"""
    expression: Any = None
    num_tokens = len(tokens)

    if len(tokens) < 3:
        raise MuffinScriptSyntaxError(UNDEFINED_VARIABLE, line_number)

    # Concatenation, token schema: ["foo, "=", "cat", "(", "hello ", bar, ")"]
    elif num_tokens > 1 and tokens[2] == "cat":
        if len(tokens) < 6 or tokens[3] != "(" or tokens[-1] != ")":
            raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
        expression = CatNode(args=tokens[4:-1], line_number=line_number)

    # Arithmetic, token schema: ["foo", "=", 2, "+", 2]
    # TODO: Support multiple arithmetic chaining
    elif num_tokens == 5 and tokens[3] in SUPPORTED_OPERATORS.keys():
        expression = ArithmeticNode(
            operator=str(tokens[3]),
            left=tokens[2],
            right=tokens[4],
            line_number=line_number,
        )

    # eg: single value, direct assignment, must come last
    elif num_tokens == 3:
        token = tokens[2]
        if isinstance(token, str) and token.startswith('"') and token.endswith('"'):
            expression = StringNode(token, line_number)
        elif token is True or token is False:
            expression = BoolNode(token, line_number)
        elif token is None:
            expression = NullNode(token, line_number)
        elif isinstance(token, int):
            expression = IntNode(token, line_number)
        elif isinstance(token, float):
            expression = FloatNode(token, line_number)

    if expression is None:
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)

    return AssignNode(
        var_name=str(tokens[0]),
        expression=expression,
        line_number=line_number,
    )
