import pytest

from muffinscript.errors import MuffinScriptSyntaxError
from muffinscript.lexer import tokenize


def test_tokenizer_newline():
    tokens = tokenize("\n", 1)
    assert tokens == []


def test_tokenizer_whitespace():
    tokens = tokenize("", 1)
    assert tokens == []

    tokens = tokenize(" ", 2)
    assert tokens == []

    tokens = tokenize("\t", 3)
    assert tokens == []

    tokens = tokenize(",", 4)
    assert tokens == []


def test_tokenizer_variables():
    tokens = tokenize('foo = "hello world"', 1)
    assert tokens == ["foo", "=", '"hello world"']


def test_tokenizer_booleans():
    tokens = tokenize("foo = true", 1)
    assert tokens == ["foo", "=", True]

    tokens = tokenize("foo = false", 2)
    assert tokens == ["foo", "=", False]


def test_tokenizer_null():
    tokens = tokenize("foo = null", 1)
    assert tokens == ["foo", "=", None]


def test_tokenizer_strings():
    tokens = tokenize('"hello world"', 1)
    assert tokens == ['"hello world"']

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize('p("hello world)', 1)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unterminated string | line: 1"


def test_tokenizer_integers():
    tokens = tokenize("foo = 2", 1)
    assert tokens == ["foo", "=", 2]


def test_tokenizer_floats():
    tokens = tokenize("foo = 2.5", 1)
    assert tokens == ["foo", "=", 2.5]

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("foo = .test", 2)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Invalid float | line: 2"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("foo = 2.3.4", 3)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Invalid float | line: 3"


def test_tokenizer_lists():
    tokens = tokenize("[1, 2, 3]", 1)
    assert tokens == ["[", 1, 2, 3, "]"]


def test_tokenizer_functions():
    tokens = tokenize('p("hello world")', 1)
    assert tokens == ["p", "(", '"hello world"', ")"]

    tokens = tokenize('cat("hello", " world")', 2)
    assert tokens == ["cat", "(", '"hello"', '" world"', ")"]

    tokens = tokenize("sleep(2.5)", 3)
    assert tokens == ["sleep", "(", 2.5, ")"]

    tokens = tokenize("type(2.5)", 4)
    assert tokens == ["type", "(", 2.5, ")"]

    tokens = tokenize("if (foo == bar) { p(true) }", 5)
    assert tokens == ["if", "(", "foo", "==", "bar", ")", "{", "p", "(", True, ")", "}"]

    tokens = tokenize("if (foo == bar) { p(true) } else { p(false) }", 6)
    # fmt: off
    assert tokens == ["if", "(", "foo", "==", "bar", ")", "{", "p", "(", True, ")", "}", "else", "{", "p", "(", False, ")", "}"]  # noqa
    # fmt: on


def test_tokenizer_arithmetic_operators():
    tokens = tokenize("foo = 2 + 2", 1)
    assert tokens == ["foo", "=", 2, "+", 2]

    tokens = tokenize("foo = 2 - 2", 2)
    assert tokens == ["foo", "=", 2, "-", 2]

    tokens = tokenize("foo = 2 * 2", 3)
    assert tokens == ["foo", "=", 2, "*", 2]

    tokens = tokenize("foo = 2 / 2", 4)
    assert tokens == ["foo", "=", 2, "/", 2]

    tokens = tokenize("foo = 2 % 1.5", 5)
    assert tokens == ["foo", "=", 2, "%", 1.5]


def test_tokenizer_comments():
    tokens = tokenize("// This is a comment", 1)  # Standalone
    assert tokens == []

    tokens = tokenize("foo = 2 // This is a comment", 2)  # Inline
    assert tokens == ["foo", "=", 2]


def test_tokenizer_relational_operators():
    tokens = tokenize("2 == 2", 1)
    assert tokens == [2, "==", 2]

    tokens = tokenize("1 != 2", 2)
    assert tokens == [1, "!=", 2]

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("!", 3)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 3"

    tokens = tokenize("2 > 1", 4)
    assert tokens == [2, ">", 1]

    tokens = tokenize("2 >= 2", 5)
    assert tokens == [2, ">=", 2]

    tokens = tokenize("1 < 2", 6)
    assert tokens == [1, "<", 2]

    tokens = tokenize("1 <= 2", 7)
    assert tokens == [1, "<=", 2]


def test_tokenizer_unsupported_statements():
    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("?", 1)
    assert str(error.value) == "\033[31mSYNTAX ERROR\033[0m - Unsupported statement | line: 1"
