import sys
import traceback


class MuffinScriptBaseError(Exception):
    """Used if MuffinScript had an issue. If the user receives this, something broke on our end.

    This should be raised if we didn't account for something and serve as the backdrop for unreachable code.
    """

    def __str__(self):
        tb = "".join(traceback.format_tb(self.__traceback__))
        msg = super().__str__()
        return f"\033[31mMUFFIN OVERFLOW\033[0m - We most likely burnt something, mind following the crumbs and reporting it?\n{msg}\n{tb}"  # noqa


class MuffinScriptSyntaxError(MuffinScriptBaseError):
    """Thrown if there are syntax errors in MuffinScript.

    This error is not intended to show a stacktrace with.
    """

    def __init__(self, message: str, line_number: int):
        self.message = message
        self.line_number = line_number
        super().__init__(message)

    def __str__(self):
        return f"\033[31mSYNTAX ERROR\033[0m - {self.message} | line: {self.line_number}"


class MuffinScriptRuntimeError(MuffinScriptBaseError):
    """Thrown if there are runtime errors in MuffinScript.

    This error is not intended to show a stacktrace with.
    """

    def __init__(self, message: str, line_number: int):
        self.message = message
        self.line_number = line_number
        super().__init__(message)

    def __str__(self):
        return f"\033[31mRUNTIME ERROR\033[0m - {self.message} | line: {self.line_number}"


def output_error(message: str):
    """Don't print stacktrace, just print message to console and exit."""
    print(message)
    sys.exit(1)
