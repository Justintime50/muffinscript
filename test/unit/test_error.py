import pytest

from muffinscript.errors import (
    MuffinScriptBaseError,
    MuffinScriptSyntaxError,
    output_error,
    output_repl_error,
)


def test_muffin_crumbs_error():
    """Test that we return the correct error message."""
    error = MuffinScriptBaseError()
    assert (
        str(error)
        == "\033[31mMUFFIN OVERFLOW\033[0m - We most likely burnt something, mind following the crumbs and reporting it?\n\n"  # noqa
    )


def test_program_syntax_error_string():
    """Test that we return an error string correctly."""
    error = MuffinScriptSyntaxError("Mock error", 1)
    assert "\033[31mSYNTAX ERROR\033[0m - Mock error" in str(error)


def test_output_error(capfd):
    """Test that we print the error message and exit the program."""
    test_message = "Mock error"
    with pytest.raises(SystemExit) as error:
        output_error(test_message)
    assert error.value.code == 1
    out, err = capfd.readouterr()
    assert test_message in out


def test_output_repl_error(capfd):
    """Test that we print the error message."""
    test_message = "Mock error"
    output_repl_error(test_message)
    out, err = capfd.readouterr()
    assert test_message in out
