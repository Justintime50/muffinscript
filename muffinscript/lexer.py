from muffinscript.constants import (
    INVALID_FLOAT,
    SUPPORTED_TYPES,
    UNSUPPORTED_STATEMENT,
    UNTERMINATED_STRINGS,
)
from muffinscript.errors import MuffinScriptSyntaxError


def tokenize(
    input: str,
    line_number: int,
) -> list[SUPPORTED_TYPES]:
    """Tokenize a line of code.

    - Skip spaces, newlines, comments
    - Ensure all characters match what is supported, break into tokens, error if not
    """
    tokens: list[SUPPORTED_TYPES] = []
    i = 0
    stripped_input = input.replace("\n", "").strip()

    while i < len(stripped_input):
        char = stripped_input[i]
        match char:
            # Variables, Booleans, and Null
            case _ if char.isalpha():
                start = i
                while i < len(stripped_input) and (stripped_input[i].isalnum()):
                    i += 1
                phrase = stripped_input[start:i]
                if phrase == "true":
                    tokens.append(True)
                elif phrase == "false":
                    tokens.append(False)
                elif phrase == "null":
                    tokens.append(None)
                else:
                    tokens.append(phrase)
            # Strings
            case '"':
                start = i + 1
                end = start
                while end < len(stripped_input) and stripped_input[end] != '"':
                    end += 1
                if end >= len(stripped_input):
                    raise MuffinScriptSyntaxError(UNTERMINATED_STRINGS, line_number)
                tokens.append('"' + stripped_input[start:end] + '"')
                i = end + 1
            # Integers and Floats
            case _ if char.isnumeric() or char == ".":
                start = i
                while i < len(stripped_input) and (stripped_input[i].isnumeric() or stripped_input[i] == "."):
                    i += 1
                if stripped_input[start:i].count(".") == 0:
                    tokens.append(int(stripped_input[start:i]))
                elif stripped_input[start:i].count(".") == 1:
                    try:
                        tokens.append(float(stripped_input[start:i]))
                    except ValueError:
                        raise MuffinScriptSyntaxError(INVALID_FLOAT, line_number)
                elif stripped_input[start:i].count(".") > 1:
                    raise MuffinScriptSyntaxError(INVALID_FLOAT, line_number)
            # Functions
            case "(":
                tokens.append("(")
                i += 1
            case ")":
                tokens.append(")")
                i += 1
            # Arithmetic Operators
            case "+":
                tokens.append("+")
                i += 1
            case "-":
                tokens.append("-")
                i += 1
            case "*":
                tokens.append("*")
                i += 1
            case "/":
                # Comments
                if stripped_input[i + 1] == "/":
                    break
                else:
                    tokens.append("/")
                    i += 1
            case "%":
                tokens.append("%")
                i += 1
            # Relational Operators
            case "=":
                if stripped_input[i + 1] == "=":
                    tokens.append("==")
                    i += 2
                else:
                    tokens.append("=")
                    i += 1
            case "!":
                if stripped_input[i + 1] == "=":
                    tokens.append("!=")
                    i += 2
                else:
                    raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)
            case ">":
                if stripped_input[i + 1] == "=":
                    tokens.append(">=")
                    i += 2
                else:
                    tokens.append(">")
                    i += 1
            case "<":
                if stripped_input[i + 1] == "=":
                    tokens.append("<=")
                    i += 2
                else:
                    tokens.append("<")
                    i += 1
            # Spaces
            case " ":
                i += 1
            # Commas
            case ",":
                i += 1
            # All else
            case _:
                raise MuffinScriptSyntaxError(UNSUPPORTED_STATEMENT, line_number)

    return tokens
