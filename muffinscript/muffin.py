import sys

from muffinscript._version import __version__
from muffinscript.constants import (
    MUFFIN_DEBUG,
    UNDEFINED_VARIABLE,
)
from muffinscript.errors import (
    MuffinScriptBaseError,
    MuffinScriptRuntimeError,
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

    with open(arg_one, "r") as code:
        code_content = code.readlines()
    variables = {}

    try:
        _run_code_block(code_content, variables, start_line=1)
    except MuffinScriptBaseError as error:
        if MUFFIN_DEBUG:
            raise error
        else:
            output_error(error)


def repl():
    """Starts the MuffinScript REPL (Read-Eval-Print Loop)."""
    try:
        import readline
    except ImportError:
        # On some systems (e.g., Windows), readline may not be available
        readline = None  # noqa

    print('MuffinScript REPL. Type "exit" to leave.')
    variables = {}
    line_number = 1

    buffer = []
    open_braces = 0
    close_braces = 0

    while True:
        try:
            prompt = "🧁 > " if not buffer else "... "
            line = input(prompt)
            if line.strip() == "exit":
                break
            buffer.append(line)
            open_braces += line.count("{")
            close_braces += line.count("}")

            # If braces are balanced, process the block
            if open_braces > 0 and open_braces == close_braces:
                code_block = buffer
                buffer = []
                open_braces = close_braces = 0
                _run_code_block(code_block, variables, start_line=line_number)
                line_number += len(code_block)
            elif open_braces == 0:
                # Single-line statement
                code_block = buffer
                buffer = []
                _run_code_block(code_block, variables, start_line=line_number)
                line_number += len(code_block)
            # else: keep buffering lines
        except MuffinScriptBaseError as error:
            output_repl_error(error)
            buffer = []
            open_braces = close_braces = 0
        except KeyboardInterrupt:
            print("\nExiting MuffinScript REPL.")
            break


def _run_code_block(code_lines, variables, start_line=1):
    """Runs a block of code, reusable for both the interpreter and REPL."""
    executable_lines = {}
    i = 0
    while i < len(code_lines):
        line = code_lines[i]
        line_number = start_line + i
        tokens = tokenize(line, line_number)
        if tokens and tokens[0] == "if":
            block_tokens = tokens[:]
            open_braces = tokens.count("{")
            close_braces = tokens.count("}")
            while open_braces > close_braces and i + 1 < len(code_lines):
                i += 1
                next_tokens = tokenize(code_lines[i], start_line + i)
                block_tokens.extend(next_tokens)
                open_braces += next_tokens.count("{")
                close_braces += next_tokens.count("}")
            # Variables must have assignment
            if len(tokens) == 1 and isinstance(tokens[0], str):
                raise MuffinScriptRuntimeError(UNDEFINED_VARIABLE, line_number)
            nodes = parse_tokens(block_tokens, line_number)
            executable_lines[str(line_number)] = nodes
        elif tokens:
            # Variables must have assignment
            if len(tokens) == 1 and isinstance(tokens[0], str):
                raise MuffinScriptRuntimeError(UNDEFINED_VARIABLE, line_number)
            nodes = parse_tokens(tokens, line_number)
            executable_lines[str(line_number)] = nodes
        i += 1

    for line_number, node in executable_lines.items():
        if node:
            evaluate(node, variables, line_number)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        output_error("Usage: muffin filename.ms")
    elif len(sys.argv) == 1:
        repl()
    else:
        main()
