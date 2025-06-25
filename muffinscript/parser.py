from muffinscript.errors import MuffinScriptSyntaxError


def parse_tokens(tokens: list[str], line_number: int) -> list[str]:
    """Parses tokens before sending them to the interpreter to ensure they have no syntax errors."""
    if len(tokens) > 1 and tokens[0] == "p":
        return _parse_print_tokens(tokens)
    elif len(tokens) > 1 and tokens[1] == "=":
        return _parse_variable_tokens(tokens)
    else:
        raise MuffinScriptSyntaxError(f"Unknown statement on line {line_number}")


def _parse_print_tokens(tokens: list[str]) -> list[str]:
    """Print tokens should look like: ["p", "(", "hello world", ")"]"""
    if len(tokens) != 4 or tokens[1] != "(" or tokens[3] != ")":
        raise MuffinScriptSyntaxError("Expected print statement in the form p(<print_arg>)")
    print_arg = tokens[2]
    if not (isinstance(print_arg, str) and print_arg):
        raise MuffinScriptSyntaxError("Can only print strings or variable names")
    return [tokens[0], print_arg]


def _parse_variable_tokens(tokens: list[str]) -> list[str]:
    """Variable tokens should look like: ["foo", "=", "hello world"]"""
    var_name = tokens[0]
    expression_tokens = tokens[2:]
    expression = _parse_expression(expression_tokens)
    return [var_name, "=", expression]


def _parse_expression(tokens: list[str]):
    # eg: single string or int
    if len(tokens) == 1:
        return tokens[0]

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
    else:
        # eg: missing assignment
        raise MuffinScriptSyntaxError("Unsupported expression")
