import pytest

from muffinscript.errors import MuffinScriptSyntaxError
from muffinscript.interpreter import evaluate_expression


def test_evaluate_prints():
    """Test that we evaluate print statements correctly."""
    expression = evaluate_expression(['p', '"hello world"'], 1, {})
    assert expression == 'hello world'

    expression = evaluate_expression(['p', 'foo'], 1, {"foo": "hello world"})
    assert expression == 'hello world'

    with pytest.raises(MuffinScriptSyntaxError) as error:
        expression = evaluate_expression(['p', '"hello world'], 2, {})
    assert (
        str(error.value)
        == "\033[31mERROR\033[0m - Undefined variable or invalid print argument on line 2: \"hello world"
    )


def test_evaluate_variable_assignment():
    """Test that we evaluate variables (there are no return values)."""
    expression = evaluate_expression(['foo', '=', '"hello world"'], 1, {})
    assert expression is None

    expression = evaluate_expression(['foo', '=', ('+', '2', '2')], 1, {})
    assert expression is None


def test_evaluate_expression():
    """Test that we evaluate expressions of variables before assignment."""
    expression = evaluate_expression(['foo', '=', '"hello world"'], 1, {"foo": "hello world"})
    assert expression is None
