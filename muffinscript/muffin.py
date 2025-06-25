import sys

from muffinscript.errors import (
    MuffinScriptSyntaxError,
    output_error,
)
from muffinscript.interpreter import evaluate_expression
from muffinscript.lexer import tokenize
from muffinscript.parser import parse_tokens


def main():
    """Runs the MuffinScript interpreter on a code file."""
    code = _get_code()
    variables = {}
    valid_lines = []

    for i, line in enumerate(code):
        line_number = i + 1

        try:
            tokens = tokenize(line, line_number)
        except MuffinScriptSyntaxError as error:
            output_error(error)

        if tokens:
            try:
                parsed_tokens = parse_tokens(tokens, line_number)
                valid_lines.append(parsed_tokens)
            except MuffinScriptSyntaxError as error:
                output_error(error)

    # Only evaluate code once the entire file has been tokenized and parsed correctly
    for i, tokens in enumerate(valid_lines):
        line_number = i + 1

        result = evaluate_expression(tokens, line_number, variables)

        if tokens and tokens[0] == 'p' and result:
            print(result)


def repl():
    """The MuffinScript REPL."""
    print('MuffinScript REPL. Type "exit" to leave.')
    variables = {}
    line_number = 1

    while True:
        try:
            line = input('🧁 > ')
            if line.strip() == 'exit':
                break
            tokens = tokenize(line, line_number)
            if tokens:
                parsed_tokens = parse_tokens(tokens, line_number)
                result = evaluate_expression(parsed_tokens, line_number, variables)
                if tokens[0] == 'p' and result:
                    print(result)
        except MuffinScriptSyntaxError as error:
            output_error(error)
        except KeyboardInterrupt:
            print('\nExiting MuffinScript REPL.')
            break


def _get_code():
    """Handles getting the code file and reading the content."""
    if len(sys.argv) > 2:
        output_error("Usage: muffin filename.ms")
    filepath = sys.argv[1]
    with open(filepath, 'r') as code:
        code_content = code.readlines()

    return code_content


if __name__ == '__main__':
    if len(sys.argv) == 1:
        repl()
    else:
        main()
