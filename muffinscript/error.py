import sys


class ProgramSyntaxError(SyntaxError):
    def __str__(self):
        # TODO: Require passing a line number here
        return f"\033[31mERROR\033[0m - {super().__str__()}"


def output_error(message: str):
    """Don't print stacktrace, just print message to console and exit."""
    print(message)
    sys.exit(1)
