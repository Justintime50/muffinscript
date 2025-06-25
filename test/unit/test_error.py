import pytest

from muffinscript.errors import (
    MuffinScriptSyntaxError,
    output_error,
)


def test_program_syntax_error_string():
    """Test that we return an error string correctly."""
    error = MuffinScriptSyntaxError("Mock error")
    assert "\033[31mERROR\033[0m - Mock error" in str(error)


def test_output_error(capfd):
    """Test that we print the error message and exit the program."""
    test_message = "Mock error"
    with pytest.raises(SystemExit) as error:
        output_error(test_message)
    assert error.value.code == 1
    out, err = capfd.readouterr()
    assert test_message in out
