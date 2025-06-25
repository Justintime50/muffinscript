import operator
from typing import Union

from muffinscript.constants import SUPPORTED_TYPES
from muffinscript.errors import MuffinCrumbsError


def evaluate_expression(
    tokens: list[Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]]],
    line_number: int,
    variables: dict[str, SUPPORTED_TYPES],
) -> SUPPORTED_TYPES | None:
    """Evaluates an expression based on the tokens used."""
    if tokens[0] == "p":
        return _evaluate_prints(tokens, line_number, variables)
    if len(tokens) > 2 and tokens[1] == "=":
        _evaluate_variable_assignment(tokens, line_number, variables)
        return None
    else:
        # If the user got here, we messed up
        raise MuffinCrumbsError()


def _evaluate_prints(
    tokens: list[Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]]],
    line_number: int,
    variables: dict[str, SUPPORTED_TYPES],
) -> SUPPORTED_TYPES:
    """Evaluates print statements.

    p("hello world")
    p(foo)
    """
    print_arg = str(tokens[1])
    # Retrieve variable
    if print_arg in variables:
        return variables[print_arg]
    if print_arg.startswith('"') and print_arg.endswith('"'):
        return print_arg.strip('"')
    # If the user got here, we messed up
    raise MuffinCrumbsError()


def _evaluate_variable_assignment(
    tokens: list[Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]]],
    line_number: int,
    variables: dict[str, SUPPORTED_TYPES],
) -> None:
    """Evaluates variable assignment.

    foo = "hello world"
    foo = 2 + 2
    """
    var_name = str(tokens[0])
    expression = tokens[2]
    value = _evaluate_expression(expression, variables)
    # Strip quotes if it's a string literal
    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    # Assign the variable
    variables[var_name] = value
    return None


def _evaluate_expression(
    expression: Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]],
    variables: dict[str, SUPPORTED_TYPES],
) -> SUPPORTED_TYPES:
    """Evaluates the expression assigned to a variable prior to assignment."""
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    if isinstance(expression, tuple) and expression[0] in operations:
        left = _evaluate_expression(expression[1], variables)
        right = _evaluate_expression(expression[2], variables)
        return operations[expression[0]](left, right)
    elif isinstance(expression, str):
        if expression in variables:
            return variables[expression]
        else:
            return expression
    elif isinstance(expression, int) or isinstance(expression, float):
        return expression
    # If the user got here, we messed up
    raise MuffinCrumbsError()
