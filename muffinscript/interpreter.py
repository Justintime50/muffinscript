import operator
from typing import Any

from muffinscript.errors import MuffinCrumbsError


def evaluate_expression(tokens: list[str], line_number: int, variables: dict[str, Any]) -> Any:
    """Evaluates an expression based on the tokens used."""
    if tokens[0] == "p":
        return _evaluate_prints(tokens, line_number, variables)
    if len(tokens) > 2 and tokens[1] == "=":
        return _evaluate_variable_assignment(tokens, line_number, variables)
    else:
        # If the user got here, we messed up
        raise MuffinCrumbsError()


def _evaluate_prints(tokens: list[str], line_number: int, variables: dict[str, Any]) -> str:
    """Evaluates print statements.

    p("hello world")
    p(foo)
    """
    print_arg = tokens[1]
    # Retrieve variable
    if print_arg in variables:
        return str(variables[print_arg])
    if print_arg.startswith('"') and print_arg.endswith('"'):
        return str(print_arg.strip('"'))
    # If the user got here, we messed up
    raise MuffinCrumbsError()


def _evaluate_variable_assignment(tokens: list[str], line_number: int, variables: dict[str, Any]) -> None:
    """Evaluates variable assignment.

    foo = "hello world"
    foo = 2 + 2
    """
    var_name = tokens[0]
    expression = tokens[2]
    value = _evaluate_expression(expression, variables)
    # Strip quotes if it's a string literal
    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    # Assign the variable
    variables[var_name] = value
    return None


def _evaluate_expression(expression: Any, variables: dict[str, Any]):
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
        # TODO: we probably shouldn't coerce this
        return operations[expression[0]](int(left), int(right))
    elif isinstance(expression, str):
        # Try to resolve variable or return as int/str
        if expression in variables:
            return variables[expression]
        try:
            return int(expression)
        except ValueError:
            return expression
    else:
        # If the user got here, we messed up
        raise MuffinCrumbsError()
