import pytest

from muffinscript.errors import MuffinScriptSyntaxError
from muffinscript.parser import parse_tokens


def test_tokens_unknown_statement():
    """Test we throw an error when an unknown statement is used."""
    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["?"], 1)
    assert str(error.value) == "\033[31mERROR\033[0m - Unknown statement on line 1"


def test_parse_print_tokens():
    """Test that we parse the `p()` function correctly."""
    parsed_tokens = parse_tokens(["p", "(", "foo", ")"], 1)
    assert parsed_tokens == ["p", "foo"]

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["p", "(", "foo"], 2)
    assert str(error.value) == "\033[31mERROR\033[0m - Expected print statement in the form p(variableName)"


def test_parse_variable_tokens():
    """Test that we parse variables correctly."""
    parsed_tokens = parse_tokens(["foo", "=", '"hello world"'], 1)
    assert parsed_tokens == ["foo", "=", '"hello world"']


def test_parse_expression():
    """Test that we parse expressions correctly."""
    parsed_tokens = parse_tokens(["foo", "=", 2, "+", 2], 1)
    assert parsed_tokens == ["foo", "=", ("+", 2, 2)]

    parsed_tokens = parse_tokens(["foo", "=", 2, "-", 2], 1)
    assert parsed_tokens == ["foo", "=", ("-", 2, 2)]

    parsed_tokens = parse_tokens(["foo", "=", 2, "*", 2], 1)
    assert parsed_tokens == ["foo", "=", ("*", 2, 2)]

    parsed_tokens = parse_tokens(["foo", "=", 2, "/", 2], 1)
    assert parsed_tokens == ["foo", "=", ("/", 2, 2)]

    parsed_tokens = parse_tokens(["foo", "=", 2.5, "+", 2.3], 1)
    assert parsed_tokens == ["foo", "=", ("+", 2.5, 2.3)]

    with pytest.raises(MuffinScriptSyntaxError) as error:
        parse_tokens(["foo", "=", "2", "?", "2"], 1)
    assert str(error.value) == "\033[31mERROR\033[0m - Unsupported expression on line 1"
