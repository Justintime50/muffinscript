# import pytest

# from muffinscript.errors import (
#     MuffinCrumbsError,
#     MuffinScriptSyntaxError,
# )
# from muffinscript.interpreter import evaluate


# def test_evaluate_expression_muffin_crumbs():
#     """Test we throw an error if MuffinScript didn't account for something."""
#     with pytest.raises(MuffinCrumbsError) as error:
#         evaluate(["?"], {})
#     assert str(error.value) == "Oh crumbs, Muffin had an issue! We most likely burnt something, not you."


# def test_evaluate_prints():
#     """Test that we evaluate print statements correctly."""
#     expression = evaluate(["p", "foo"], {"foo": "hello world"})
#     assert expression == "hello world"

#     expression = evaluate(["p", "foo"], {"foo": "true"})
#     assert expression == "true"

#     expression = evaluate(["p", "foo"], {"foo": "false"})
#     assert expression == "false"

#     expression = evaluate(["p", "foo"], {"foo": "null"})
#     assert expression == "null"


# def test_evaluate_variable_assignment():
#     """Test that we evaluate variables (there are no return values)."""
#     expression = evaluate(["foo", "=", '"hello world"'], {})
#     assert expression is None

#     expression = evaluate(["foo", "=", ("+", "2", "2")], {})
#     assert expression is None


# def test_evaluate_expression():
#     """Test that we evaluate expressions of variables before assignment."""
#     expression = evaluate(["foo", "=", '"hello world"'], {"foo": "hello world"})
#     assert expression is None

#     with pytest.raises(MuffinCrumbsError) as error:
#         evaluate(["foo", "=", ("?", "2", "2")], {})
#     assert str(error.value) == "Oh crumbs, Muffin had an issue! We most likely burnt something, not you."

#     with pytest.raises(MuffinScriptSyntaxError) as error:
#         evaluate(["foo", "=", ("+", "true", "2")], {})
#     assert str(error.value) == "\033[31mERROR\033[0m - Invalid expression | line: 3"
