import pytest

from muffinscript.errors import MuffinScriptSyntaxError
from muffinscript.lexer import tokenize


def test_tokenizer():
    """Test that we tokenize all supported tokens correctly."""
    tokens = tokenize("// This is a comment", 1)
    assert tokens == []

    tokens = tokenize("\n", 2)
    assert tokens == []

    tokens = tokenize('foo = "hello world"', 3)
    assert tokens == ["foo", "=", '"hello world"']

    tokens = tokenize('p("hello world")', 4)
    assert tokens == ["p", "(", '"hello world"', ")"]

    tokens = tokenize("foo = 2 + 2", 5)
    assert tokens == ["foo", "=", 2, "+", 2]

    tokens = tokenize("foo = 2 - 2", 6)
    assert tokens == ["foo", "=", 2, "-", 2]

    tokens = tokenize("foo = 2 * 2", 7)
    assert tokens == ["foo", "=", 2, "*", 2]

    tokens = tokenize("foo = 2 / 2", 8)
    assert tokens == ["foo", "=", 2, "/", 2]

    tokens = tokenize("foo = 2 % 1.5", 9)
    assert tokens == ["foo", "=", 2, "%", 1.5]

    tokens = tokenize("foo = 2.5", 10)
    assert tokens == ["foo", "=", 2.5]

    tokens = tokenize("foo = true", 11)
    assert tokens == ["foo", "=", True]

    tokens = tokenize("foo = false", 12)
    assert tokens == ["foo", "=", False]

    tokens = tokenize("foo = null", 13)
    assert tokens == ["foo", "=", None]

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("foo = .test", 14)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Invalid float | line: 14"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("foo = 2.3.4", 15)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Invalid float | line: 15"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("?", 16)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 16"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize('p("hello world)', 17)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unterminated string | line: 17"

    tokens = tokenize("if (foo == bar) { p(true) }", 18)
    assert tokens == ["if", "(", "foo", "==", "bar", ")", "{", "p", "(", True, ")", "}"]

    tokens = tokenize("if (foo == bar) { p(true) } else { p(false) }", 19)
    # fmt: off
    assert tokens == ["if", "(", "foo", "==", "bar", ")", "{", "p", "(", True, ")", "}", "else", "{", "p", "(", False, ")", "}"]  # noqa
    # fmt: on
