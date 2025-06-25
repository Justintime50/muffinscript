from muffinscript.constants import SUPPORTED_TYPES
from muffinscript.errors import MuffinScriptSyntaxError


def tokenize(input: str, line_number: int) -> list[SUPPORTED_TYPES]:
    """Tokenize a line of code.

    - Skip spaces and newlines
    - Skip comments
    - Ensure all characters match what is supported, error if not
    """
    tokens: list[SUPPORTED_TYPES] = []
    i = 0

    stripped_input = input.replace("\n", "").strip()

    # Ignore empty lines
    if not stripped_input:
        return []

    while i < len(stripped_input):
        char = stripped_input[i]
        match char:
            # Variables and Booleans
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
                    raise MuffinScriptSyntaxError(f"Unterminated string on line {line_number}")
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
                        raise MuffinScriptSyntaxError(f"Invalid float on line {line_number}")
                else:
                    raise MuffinScriptSyntaxError(f"Invalid float on line {line_number}")
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
                    raise MuffinScriptSyntaxError(f"Unknown token on line {line_number}: {stripped_input[i]}")
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
            # All else
            case _:
                raise MuffinScriptSyntaxError(f"Unknown token on line {line_number}: {stripped_input[i]}")

    return tokens
