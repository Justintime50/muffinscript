from typing import Union

from muffinscript.constants import (
    SUPPORTED_OPERATORS,
    SUPPORTED_TYPES,
)
from muffinscript.errors import (
    MuffinCrumbsError,
    MuffinScriptSyntaxError,
)


def evaluate_tokens(
    tokens: list[Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]]],
    line_number: int,
    variables: dict[str, SUPPORTED_TYPES],
) -> SUPPORTED_TYPES | None:
    """Evaluates tokens to determine what to run."""
    if tokens[0] == "p":
        return _evaluate_prints(tokens, line_number, variables)
    if len(tokens) > 2 and tokens[1] == "=":
        _evaluate_variable_assignment(tokens, line_number, variables)
        return None
    # If the user got here, we messed up
    raise MuffinCrumbsError()


def _evaluate_prints(
    tokens: list[Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]]],
    line_number: int,
    variables: dict[str, SUPPORTED_TYPES],
) -> SUPPORTED_TYPES:
    """Evaluates print statements.

    foo = "hello world"
    p(foo)
    """
    print_arg = str(tokens[1])
    if print_arg in variables:
        return variables[print_arg]
    else:
        raise MuffinScriptSyntaxError(f"Undefined variable {print_arg} on line {line_number}")
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
    value = _evaluate_expression(expression, line_number, variables)
    # Strip quotes if it's a string literal
    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    # Assign the variable
    variables[var_name] = value
    return None


def _evaluate_expression(
    expression: Union[SUPPORTED_TYPES, tuple[str, SUPPORTED_TYPES, SUPPORTED_TYPES]],
    line_number: int,
    variables: dict[str, SUPPORTED_TYPES],
) -> SUPPORTED_TYPES:
    """Evaluates the expression assigned to a variable prior to assignment."""
    if isinstance(expression, tuple) and expression[0] in SUPPORTED_OPERATORS:
        left = _evaluate_expression(expression[1], line_number, variables)
        right = _evaluate_expression(expression[2], line_number, variables)
        try:
            float(str(left))
            float(str(right))
        except ValueError:
            raise MuffinScriptSyntaxError(f"Invalid arithmetic expression at line {line_number}")
        evaluation = SUPPORTED_OPERATORS[expression[0]](left, right)
        if evaluation is True:
            return "true"
        elif evaluation is False:
            return "false"
        elif evaluation is None:
            return "null"
        else:
            return evaluation
    elif isinstance(expression, str):
        if expression in variables:
            return variables[expression]
        else:
            return expression
    elif isinstance(expression, int) or isinstance(expression, float):
        return expression
    # If the user got here, we messed up
    raise MuffinCrumbsError()
