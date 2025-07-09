import sys

from muffinscript._version import __version__
from muffinscript.constants import MUFFIN_DEBUG
from muffinscript.errors import (
    MuffinScriptBaseError,
    output_error,
    output_repl_error,
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
        i = 0
        while i < len(code):
            line = code[i]
            line_number = i + 1
            tokens = tokenize(line, line_number)
            # If this line starts an if statement, buffer until the block(s) close
            if tokens and tokens[0] == "if":
                block_tokens = tokens[:]
                open_braces = tokens.count("{")
                close_braces = tokens.count("}")
                # Keep reading lines until all blocks are closed
                while open_braces > close_braces and i + 1 < len(code):
                    i += 1
                    next_tokens = tokenize(code[i], i + 1)
                    block_tokens.extend(next_tokens)
                    open_braces += next_tokens.count("{")
                    close_braces += next_tokens.count("}")
                # Check for else after if block
                if i + 1 < len(code):
                    next_line_tokens = tokenize(code[i + 1], i + 2)
                    if next_line_tokens and next_line_tokens[0] == "else":
                        i += 1
                        block_tokens.extend(next_line_tokens)
                        open_braces += next_line_tokens.count("{")
                        close_braces += next_line_tokens.count("}")
                        # Buffer else block
                        while open_braces > close_braces and i + 1 < len(code):
                            i += 1
                            next_tokens = tokenize(code[i], i + 1)
                            block_tokens.extend(next_tokens)
                            open_braces += next_tokens.count("{")
                            close_braces += next_tokens.count("}")
                nodes = parse_tokens(block_tokens, line_number)
                executable_lines[str(line_number)] = nodes
            elif tokens:
                nodes = parse_tokens(tokens, line_number)
                executable_lines[str(line_number)] = nodes
            i += 1

        # Only evaluate code once the entire file has been tokenized and parsed correctly
        for line_number, node in executable_lines.items():
            if node:
                evaluate(node, variables, line_number)
    except MuffinScriptBaseError as error:
        if MUFFIN_DEBUG:
            raise error
        else:
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
        except MuffinScriptBaseError as error:
            output_repl_error(error)
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
