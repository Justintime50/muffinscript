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
    StringNode,
)
from muffinscript.constants import (
    SUPPORTED_OPERATORS,
    SUPPORTED_TYPES,
)


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
    else:
        if node in variables:
            return variables[node]

    # TODO: Should we be setting these back to a nodes?
    return node
