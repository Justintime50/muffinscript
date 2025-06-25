from typing import Any

from muffinscript.errors import ProgramSyntaxError


def evaluate_expression(tokens: list[str], line_number: int, variables: dict[str, Any]) -> Any:
    if tokens[0] == "p":
        return _evaluate_prints(tokens, line_number, variables)
    if len(tokens) > 1 and tokens[1] == "=":
        return _evaluate_variable_assignment(tokens, line_number, variables)
    else:
        raise ProgramSyntaxError("Unsupported expression")


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
    raise ProgramSyntaxError(f"Undefined variable or invalid print argument on line {line_number}: {print_arg}")


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
    variables[var_name] = value
    return None


def _evaluate_expression(expression: Any, variables: dict[str, Any]):
    """Evaluates the expression assigned to a variable prior to assignment."""
    if isinstance(expression, tuple) and expression[0] == "+":
        left = _evaluate_expression(expression[1], variables)
        right = _evaluate_expression(expression[2], variables)
        return int(left) + int(right)  # TODO: we probably shouldn't coerce this
    elif isinstance(expression, tuple) and expression[0] == "-":
        left = _evaluate_expression(expression[1], variables)
        right = _evaluate_expression(expression[2], variables)
        return int(left) - int(right)  # TODO: we probably shouldn't coerce this
    elif isinstance(expression, tuple) and expression[0] == "*":
        left = _evaluate_expression(expression[1], variables)
        right = _evaluate_expression(expression[2], variables)
        return int(left) * int(right)  # TODO: we probably shouldn't coerce this
    elif isinstance(expression, tuple) and expression[0] == "/":
        left = _evaluate_expression(expression[1], variables)
        right = _evaluate_expression(expression[2], variables)
        return int(left) / int(right)  # TODO: we probably shouldn't coerce this
    elif isinstance(expression, str):
        # Try to resolve variable or return as int/str
        if expression in variables:
            return variables[expression]
        try:
            return int(expression)
        except ValueError:
            return expression
    else:
        raise ProgramSyntaxError("Unsupported expression")
