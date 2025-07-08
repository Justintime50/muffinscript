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
    SleepNode,
    StringNode,
)
from muffinscript.ast.base import IfNode
from muffinscript.ast.standard_lib import TypeCheckNode
from muffinscript.constants import (
    INVALID_COERCION,
    INVALID_FLOAT,
    SUPPORTED_OPERATORS,
    SUPPORTED_TYPES,
    UNDEFINED_VARIABLE,
    UNSUPPORTED_STATEMENT,
)
from muffinscript.errors import (
    MuffinScriptRuntimeError,
    MuffinScriptSyntaxError,
)


def parse_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> Any:
    """Parses tokens before sending them to the interpreter to ensure they have no syntax errors."""
    # We begin by parsing top-level statements, if we can't match one we start parsing expressions.
    # Print
    if "p" == tokens[0]:
        return _parse_print_tokens(tokens, line_number)
    # Variables
    elif len(tokens) > 1 and "=" == tokens[1]:
        return _parse_variable_tokens(tokens, line_number)
    # Sleep
    elif "sleep" == tokens[0]:
        return _parse_sleep_tokens(tokens, line_number)
    # If statements
    elif "if" == tokens[0]:
        return _parse_if_tokens(tokens, line_number)
    # All other expressions that need evaluation
    else:
        return _parse_expression(tokens, line_number)


def _parse_print_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> PrintNode:
    """Token schema: ["p", "(", "foo", ")"]"""
    _validate_function_schema(tokens, line_number, "p", 4)
    if len(tokens) == 4 and isinstance(tokens[2], str):
        # Using a variable
        expression: Any = tokens[2]
    else:
        # Using an expression
        expression = parse_tokens(tokens[2:-1], line_number)
    return PrintNode(expression, line_number)


def _parse_variable_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> AssignNode:
    """Token schema: ["foo", "=", "hello world"]"""
    expression: Any = None
    if len(tokens) < 3:
        raise MuffinScriptSyntaxError(UNDEFINED_VARIABLE, line_number)
    expression = parse_tokens(tokens[2:], line_number)
    return AssignNode(
        var_name=str(tokens[0]),
        expression=expression,
        line_number=line_number,
    )


def _parse_sleep_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> BaseNode:
    """Token schema: ["sleep", "(", 2.5, ")"]"""
    _validate_function_schema(tokens, line_number, "sleep", 4)
    if not isinstance(tokens[2], (str, int, float)):  # Allow str for variable names
        raise MuffinScriptSyntaxError(INVALID_FLOAT, line_number)
    return SleepNode(tokens[2], line_number)


def _parse_if_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> BaseNode:
    """Token schema: ["if", "(", "foo", "=", "bar", ")", "{", ...]

    Note that if statement tokens may not occur on the same line because the opening and closing brackets
    could occur on different lines.
    """
    if tokens[0] != "if" or len(tokens) < 4 or tokens[1] != "(" or ")" not in tokens or "{" not in tokens:
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)

    # Condition
    condition = None
    open_paren_idx = next((i for i, token in enumerate(tokens) if token == "("), None)  # nosec
    close_paren_idx = next((i for i, token in enumerate(tokens) if token == ")"), None)  # nosec
    if open_paren_idx is not None and close_paren_idx is not None and close_paren_idx > open_paren_idx:
        inner_tokens = tokens[open_paren_idx + 1 : close_paren_idx]
        condition = parse_tokens(inner_tokens, line_number)

    # Body
    body = []
    open_body_idx = next((i for i, token in enumerate(tokens) if token == "{"), None)  # nosec
    close_body_idx = next((i for i, token in enumerate(tokens) if token == "}"), None)  # nosec
    if open_body_idx is not None and close_body_idx is not None and close_body_idx > open_body_idx:
        inner_tokens = tokens[open_body_idx + 1 : close_body_idx]
        body.append(parse_tokens(inner_tokens, line_number))

    return IfNode(condition, body, line_number)


def _parse_expression(tokens: list[Any], line_number: int) -> BaseNode:
    """Parses an expression from provided tokens."""
    # String concatenation
    if tokens[0] == "cat":
        _validate_function_schema(tokens, line_number, "cat", 4)
        return CatNode(args=[parse_tokens([token], line_number) for token in tokens[2:-1]], line_number=line_number)
    # Coercion
    elif "str" in tokens or "int" in tokens or "float" in tokens:
        return _parse_coercion_tokens(tokens, line_number)
    # Type check
    elif "type" in tokens:
        return _parse_type_check_tokens(tokens, line_number)
    # Arithmetic
    elif len(tokens) == 3 and tokens[1] in SUPPORTED_OPERATORS.keys():
        # TODO: Support multiple arithmetic chaining
        return ArithmeticNode(
            operator=str(tokens[1]),
            left=tokens[0],
            right=tokens[2],
            line_number=line_number,
        )
    # Single value expressions
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

    raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)


def _parse_coercion_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> BaseNode:
    """Token schema: ["str", "(", 2, ")"] or ["int", "(", "2", ")"] or ["float", "(", "2.5", ")"]"""
    value: Any = None
    if tokens[0] == "str":
        _validate_function_schema(tokens, line_number, "str", 4)
        value = str(tokens[2])
        return StringNode(value, line_number)
    elif tokens[0] == "int":
        _validate_function_schema(tokens, line_number, "int", 4)
        try:
            value = int(tokens[2].replace('"', ""))  # type:ignore
        except ValueError:
            raise MuffinScriptRuntimeError(INVALID_COERCION, line_number)
        return IntNode(value, line_number)
    elif tokens[0] == "float":
        _validate_function_schema(tokens, line_number, "float", 4)
        try:
            value = float(tokens[2])  # type:ignore
        except ValueError:
            raise MuffinScriptRuntimeError(INVALID_COERCION, line_number)
        return FloatNode(value, line_number)
    raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)


def _parse_type_check_tokens(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
) -> BaseNode:
    """Token schema: ["type", "(", "foo", ")"]"""
    _validate_function_schema(tokens, line_number, "type", 4)
    if len(tokens) == 4 and isinstance(tokens[2], str):
        # Using a variable
        expression: Any = tokens[2]
    else:
        # Using an expression
        expression = parse_tokens(tokens[2:-1], line_number)
    return TypeCheckNode(expression, line_number)


def _validate_function_schema(
    tokens: list[SUPPORTED_TYPES],
    line_number: int,
    function_name: str,
    min_tokens_lenth: int = 4,
):
    """Validates the schema of a function call."""
    if tokens[0] != function_name or len(tokens) < min_tokens_lenth or tokens[1] != "(" or tokens[-1] != ")":
        raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
