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

    tokens = tokenize("foo = 2.5", 9)
    assert tokens == ["foo", "=", 2.5]

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("foo = .test", 10)
    assert str(error.value) == "\033[31mERROR\033[0m - Invalid float on line 10"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("foo = 2.3.4", 11)
    assert str(error.value) == "\033[31mERROR\033[0m - Invalid float on line 11"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize("?", 9)
    assert str(error.value) == "\033[31mERROR\033[0m - Unknown token on line 9: ?"

    with pytest.raises(MuffinScriptSyntaxError) as error:
        tokenize('p("hello world)', 10)
    assert str(error.value) == "\033[31mERROR\033[0m - Unterminated string on line 10"
