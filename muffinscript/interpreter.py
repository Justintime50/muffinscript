import time
from typing import Any

from muffinscript.ast import (
    ArithmeticNode,
    AssignNode,
    BoolNode,
    CatNode,
    FloatNode,
    IntNode,
    NullNode,
    PrintNode,
    SleepNode,
    StringNode,
)
from muffinscript.ast.standard_lib import TypeCheckNode
from muffinscript.constants import (
    PYTHON_TO_MUFFIN_TYPES,
    SUPPORTED_OPERATORS,
    SUPPORTED_TYPES,
)
from muffinscript.errors import MuffinScriptBaseError


def evaluate(node: Any, variables: dict[str, SUPPORTED_TYPES]) -> SUPPORTED_TYPES:
    """Evaluates tokens to determine what to run."""
    if isinstance(node, PrintNode):
        print(evaluate(node.value, variables))
    elif isinstance(node, AssignNode):
        variables[node.var_name] = evaluate(node.expression, variables)
    elif isinstance(node, StringNode):
        return node.value
    elif isinstance(node, IntNode):
        return node.value
    elif isinstance(node, FloatNode):
        return node.value
    elif isinstance(node, BoolNode):
        return node.value
    elif isinstance(node, NullNode):
        return "null"
    elif isinstance(node, ArithmeticNode):
        left = evaluate(node.left, variables)
        right = evaluate(node.right, variables)
        return str(SUPPORTED_OPERATORS[node.operator](left, right)).lower()
    elif isinstance(node, CatNode):
        return "".join([arg.value for arg in node.args])
    elif isinstance(node, SleepNode):
        time.sleep(evaluate(node.duration, variables))  # type:ignore
    elif isinstance(node, TypeCheckNode):
        python_type = type(evaluate(node.value, variables))
        muffin_type = PYTHON_TO_MUFFIN_TYPES.get(python_type)
        if muffin_type is None:
            raise MuffinScriptBaseError()
        return muffin_type
    else:
        if node in variables:
            return variables[node]

    # TODO: Should we be setting these back to a nodes?
    return node
