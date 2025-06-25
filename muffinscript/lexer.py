from muffinscript.constants import SUPPORTED_TYPES
from muffinscript.errors import MuffinScriptSyntaxError


def tokenize(input: str, line_number: int) -> list[SUPPORTED_TYPES]:
    """Tokenize a line of code.

    - Ensure all characters match what is supported, error if not
    - Skip spaces
    - Strip newline characters
    """
    tokens: list[SUPPORTED_TYPES] = []
    i = 0

    sanitized_input = input.replace("\n", "").strip()

    if sanitized_input == "":
        # Ignore empty lines
        return []
    # TODO: Add support for inline comments
    if sanitized_input.startswith("//"):
        # Ignore comments
        return []

    while i < len(sanitized_input):
        char = sanitized_input[i]
        match char:
            # Variables
            # Bools magically work in this, thanks Python
            case _ if char.isalpha():
                start = i
                while i < len(sanitized_input) and (sanitized_input[i].isalnum()):
                    i += 1
                tokens.append(sanitized_input[start:i])
            # Strings
            case '"':
                start = i + 1
                end = start
                while end < len(sanitized_input) and sanitized_input[end] != '"':
                    end += 1
                if end >= len(sanitized_input):
                    raise MuffinScriptSyntaxError(f"Unterminated string on line {line_number}")
                tokens.append('"' + sanitized_input[start:end] + '"')
                i = end + 1
            # Integers and Floats
            case _ if char.isnumeric() or char == ".":
                start = i
                while i < len(sanitized_input) and (sanitized_input[i].isnumeric() or sanitized_input[i] == "."):
                    i += 1
                if sanitized_input[start:i].count(".") == 0:
                    tokens.append(int(sanitized_input[start:i]))
                elif sanitized_input[start:i].count(".") == 1:
                    try:
                        tokens.append(float(sanitized_input[start:i]))
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
            # Operators
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
                tokens.append("/")
                i += 1
            # Assignment
            case "=":
                tokens.append("=")
                i += 1
            # Spaces
            case " ":
                i += 1
            # All else
            case _:
                raise MuffinScriptSyntaxError(f"Unknown token on line {line_number}: {sanitized_input[i]}")

    return tokens
