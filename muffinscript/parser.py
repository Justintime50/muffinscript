from typing import Union

from muffinscript.constants import SUPPORTED_TYPES
from muffinscript.errors import MuffinScriptSyntaxError


def parse_tokens(
    tokens: list[SUPPORTED_TYPES], line_number: int
) -> list[Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]]]:
    """Parses tokens before sending them to the interpreter to ensure they have no syntax errors."""
    if len(tokens) > 1 and tokens[0] == "p":
        return _parse_print_tokens(tokens, line_number)
    elif len(tokens) > 1 and tokens[1] == "=":
        return _parse_variable_tokens(tokens, line_number)
    else:
        raise MuffinScriptSyntaxError(f"Unknown statement on line {line_number}")


def _parse_print_tokens(
    tokens: list[SUPPORTED_TYPES], line_number: int
) -> list[Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]]]:
    """Print tokens should look like: ["p", "(", "hello world", ")"]"""
    if len(tokens) != 4 or tokens[1] != "(" or tokens[3] != ")":
        raise MuffinScriptSyntaxError("Expected print statement in the form p(<print_arg>)")
    print_arg = tokens[2]
    if not (isinstance(print_arg, str) and print_arg):
        raise MuffinScriptSyntaxError("Can only print strings or variable names")
    return [tokens[0], print_arg]


def _parse_variable_tokens(
    tokens: list[SUPPORTED_TYPES], line_number: int
) -> list[SUPPORTED_TYPES | tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]]:
    """Variable tokens should look like: ["foo", "=", "hello world"]"""
    var_name = tokens[0]
    expression_tokens = tokens[2:]
    expression = _parse_expression(expression_tokens, line_number)
    return [var_name, "=", expression]


def _parse_expression(
    tokens: list[SUPPORTED_TYPES], line_number: int
) -> SUPPORTED_TYPES | tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]:
    """Parse the expression of a variable before assignment."""
    # eg: single string or int
    if len(tokens) == 1:
        token = tokens[0]

        if (
            (isinstance(token, str) and token.startswith('"') and token.endswith('"'))
            or token is True
            or token is False
            or token is None
            or isinstance(token, int)
            or isinstance(token, float)
        ):
            return token

    # TODO: Support multiple arithmetic chaining
    elif len(tokens) == 3 and tokens[1] == "+":
        left = tokens[0]
        right = tokens[2]
        return ("+", left, right)  # tuple to distinguish type of expression in interpreter
    elif len(tokens) == 3 and tokens[1] == "-":
        left = tokens[0]
        right = tokens[2]
        return ("-", left, right)  # tuple to distinguish type of expression in interpreter
    elif len(tokens) == 3 and tokens[1] == "*":
        left = tokens[0]
        right = tokens[2]
        return ("*", left, right)  # tuple to distinguish type of expression in interpreter
    elif len(tokens) == 3 and tokens[1] == "/":
        left = tokens[0]
        right = tokens[2]
        return ("/", left, right)  # tuple to distinguish type of expression in interpreter

    # eg: missing assignment
    raise MuffinScriptSyntaxError(f"Unsupported expression on line {line_number}")
