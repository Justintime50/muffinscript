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
        value = evaluate(node.value, variables)
        print(value)
    elif isinstance(node, AssignNode):
        variables[node.var_name] = evaluate(node.expression, variables)
    elif isinstance(node, StringNode):
        # Strip quotes if it's a string literal
        if isinstance(node.value, str) and node.value.startswith('"') and node.value.endswith('"'):
            value = node.value[1:-1]
        else:
            value = node.value
        return str(value)
    elif isinstance(node, IntNode):
        return int(node.value)
    elif isinstance(node, FloatNode):
        return float(node.value)
    elif isinstance(node, BoolNode):
        return str(bool(node.value)).lower()
    elif isinstance(node, NullNode):
        return "null"
    elif isinstance(node, ArithmeticNode):
        left = evaluate(node.left, variables)
        right = evaluate(node.right, variables)
        return str(SUPPORTED_OPERATORS[node.operator](left, right)).lower()
    elif isinstance(node, CatNode):
        args_to_cat: list[str] = []
        for arg in node.args:
            if arg in variables:
                arg = variables[arg]
            args_to_cat.append(str(evaluate(StringNode(arg, 0), variables)))
        return "".join(args_to_cat)
    else:
        if node in variables:
            return variables[node]

    return node
