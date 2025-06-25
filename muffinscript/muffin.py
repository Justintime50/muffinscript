import sys

from muffinscript import (
    ProgramSyntaxError,
    evaluate_expression,
    output_error,
    parse_tokens,
    tokenize,
)


def main():
    code = _get_code()
    variables = {}

    for i, line in enumerate(code):
        line_number = i + 1

        try:
            tokens = tokenize(line, line_number)
        except ProgramSyntaxError as error:
            output_error(error)

        if tokens:
            try:
                parsed_tokens = parse_tokens(tokens, line_number)
            except ProgramSyntaxError as error:
                output_error(error)

            try:
                result = evaluate_expression(parsed_tokens, line_number, variables)
            except ProgramSyntaxError as error:
                output_error(error)

            if parsed_tokens and parsed_tokens[0] == "p" and result:
                print(result)


def _get_code():
    if len(sys.argv) < 2:
        print("Usage: muffin filename.ms")
        sys.exit(1)
    filepath = sys.argv[1]
    with open(filepath, "r") as code:
        code_content = code.readlines()

    return code_content


if __name__ == "__main__":
    main()
