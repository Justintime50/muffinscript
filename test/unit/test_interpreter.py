import pytest

from muffinscript.errors import MuffinCrumbsError
from muffinscript.interpreter import evaluate_expression


def test_evaluate_expression_muffin_crumbs():
    """Test we throw an error if MuffinScript didn't account for something."""
    with pytest.raises(MuffinCrumbsError) as error:
        evaluate_expression(['?'], 1, {})
    assert str(error.value) == "Oh crumbs, Muffin had an issue! We most likely burnt something, not you."


def test_evaluate_prints():
    """Test that we evaluate print statements correctly."""
    expression = evaluate_expression(['p', '"hello world"'], 1, {})
    assert expression == 'hello world'

    expression = evaluate_expression(['p', 'foo'], 1, {"foo": "hello world"})
    assert expression == 'hello world'

    with pytest.raises(MuffinCrumbsError) as error:
        evaluate_expression(['p', '"hello world'], 2, {})
    assert str(error.value) == "Oh crumbs, Muffin had an issue! We most likely burnt something, not you."


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

    with pytest.raises(MuffinCrumbsError) as error:
        evaluate_expression(['foo', '=', ('?', '2', '2')], 2, {})
    assert str(error.value) == "Oh crumbs, Muffin had an issue! We most likely burnt something, not you."
