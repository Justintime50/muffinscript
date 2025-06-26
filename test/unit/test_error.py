import pytest

from muffinscript.errors import (
    MuffinCrumbsError,
    MuffinScriptSyntaxError,
    output_error,
)


def test_muffin_crumbs_error():
    """Test that we return the correct error message."""
    error = MuffinCrumbsError()
    assert str(error) == "Oh crumbs, Muffin had an issue! We most likely burnt something, not you."


def test_program_syntax_error_string():
    """Test that we return an error string correctly."""
    error = MuffinScriptSyntaxError("Mock error", 1)
    assert "\033[31mERROR\033[0m - Mock error" in str(error)


def test_output_error(capfd):
    """Test that we print the error message and exit the program."""
    test_message = "Mock error"
    with pytest.raises(SystemExit) as error:
        output_error(test_message)
    assert error.value.code == 1
    out, err = capfd.readouterr()
    assert test_message in out
    assert test_message in out
