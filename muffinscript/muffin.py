import sys

from muffinscript._version import __version__
from muffinscript.errors import (
    MuffinScriptSyntaxError,
    output_error,
)
from muffinscript.interpreter import evaluate
from muffinscript.lexer import tokenize
from muffinscript.parser import parse_tokens


def main():
    """Runs the MuffinScript interpreter on a code file."""
    arg_one = sys.argv[1]
    if arg_one == "--version":
        print(f"Muffin: v{__version__}")
        sys.exit()
    elif arg_one == "--help":
        print("Baking instructions can be found at https://github.com/justintime50/muffinscript")
        sys.exit()

    code = _get_code(arg_one)
    variables = {}
    executable_lines = {}  # Stores key as line number, value as executable line (if valid)

    try:
        for i, line in enumerate(code):
            line_number = i + 1
            executable_lines[str(line_number)] = None

            tokens = tokenize(line, line_number)
            if tokens:
                nodes = parse_tokens(tokens, line_number)
                executable_lines[str(line_number)] = nodes

        # Only evaluate code once the entire file has been tokenized and parsed correctly
        for line_number, node in executable_lines.items():
            if node:
                evaluate(node, variables)
    except MuffinScriptSyntaxError as error:
        output_error(error)


def repl():
    """The MuffinScript REPL."""
    print('MuffinScript REPL. Type "exit" to leave.')
    variables = {}
    line_number = 1

    while True:
        try:
            line = input("🧁 > ")
            if line.strip() == "exit":
                break
            tokens = tokenize(line, line_number)
            if tokens:
                nodes = parse_tokens(tokens, line_number)
                evaluate(nodes, line_number, variables)
        except MuffinScriptSyntaxError as error:
            output_error(error)
        except KeyboardInterrupt:
            print("\nExiting MuffinScript REPL.")
            break


def _get_code(filepath: str):
    """Handles getting the code file and reading the content."""
    with open(filepath, "r") as code:
        code_content = code.readlines()

    return code_content


if __name__ == "__main__":
    if len(sys.argv) > 2:
        output_error("Usage: muffin filename.ms")
    elif len(sys.argv) == 1:
        repl()
    else:
        main()
