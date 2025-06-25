import sys


class MuffinCrumbsError(Exception):
    """Used if MuffinScript had an issue. If the user receives this, something broke on our end.

    This should be raised if we didn't account for something and serve as the backdrop for unreachable code.

    This error should definitely show the stacktrace so we can track where in the language we hit a snag.
    """

    def __str__(self):
        return "Oh crumbs, Muffin had an issue! We most likely burnt something, not you."


class MuffinScriptSyntaxError(SyntaxError):
    """Thrown if there are syntax errors in MuffinScript.

    This error is not intended to show a stacktrace with.
    """

    def __init__(self, message: str, line_number: int):
        self.message = message
        self.line_number = line_number
        super().__init__(message)

    def __str__(self):
        return f"\033[31mERROR\033[0m - {self.message} | line: {self.line_number}"


def output_error(message: str):
    """Don't print stacktrace, just print message to console and exit."""
    print(message)
    sys.exit(1)
