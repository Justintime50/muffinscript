from muffinscript.errors import MuffinScriptSyntaxError


def tokenize(input: str, line_number: int) -> list:
    """Tokenize a line of code.

    - Ensure all characters match what is supported, error if not
    - Skip spaces
    - Strip newline characters
    """
    tokens = []
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
            case _ if char.isalpha():
                start = i
                while i < len(sanitized_input) and (sanitized_input[i].isalnum()):
                    i += 1
                tokens.append(sanitized_input[start:i])
            case _ if char.isnumeric():
                start = i
                while i < len(sanitized_input) and (sanitized_input[i].isnumeric()):
                    i += 1
                tokens.append(sanitized_input[start:i])
            case "(":
                tokens.append("(")
                i += 1
            case ")":
                tokens.append(")")
                i += 1
            case '"':
                start = i + 1
                end = start
                while end < len(sanitized_input) and sanitized_input[end] != '"':
                    end += 1
                if end >= len(sanitized_input):
                    raise MuffinScriptSyntaxError(f"Unterminated string on line {line_number}")
                tokens.append('"' + sanitized_input[start:end] + '"')
                i = end + 1
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
            case "=":
                tokens.append("=")
                i += 1
            case " ":
                i += 1
            case _:
                raise MuffinScriptSyntaxError(f"Unknown token on line {line_number}: {sanitized_input[i]}")

    return tokens
