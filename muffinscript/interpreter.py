import re
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
from muffinscript.ast.base import IfNode
from muffinscript.ast.standard_lib import TypeCheckNode
from muffinscript.constants import (
    PYTHON_TO_MUFFIN_TYPES,
    SUPPORTED_OPERATORS,
    SUPPORTED_TYPES,
    UNDEFINED_VARIABLE,
)
from muffinscript.errors import (
    MuffinScriptBaseError,
    MuffinScriptRuntimeError,
)


def evaluate(node: Any, variables: dict[str, SUPPORTED_TYPES]) -> SUPPORTED_TYPES:
    """Evaluates tokens to determine what to run."""
    if isinstance(node, PrintNode):
        print(evaluate(node.value, variables))
    elif isinstance(node, AssignNode):
        variables[node.var_name] = evaluate(node.expression, variables)
    elif isinstance(node, StringNode):
        # String interpolation
        variables_to_replace = re.findall(r"#\{(.*?)}", str(node.value))
        if variables_to_replace:
            for var in variables_to_replace:
                if var in variables:
                    node.value = str(node.value).replace(f"#{{{var}}}", str(variables[var]))
                else:
                    # TODO: We don't have the line number here
                    raise MuffinScriptRuntimeError(UNDEFINED_VARIABLE, 0)
        return node.value
    elif isinstance(node, IntNode):
        return node.value
    elif isinstance(node, FloatNode):
        return node.value
    elif isinstance(node, BoolNode):
        return node.value
    elif isinstance(node, NullNode):
        return node.value
    elif isinstance(node, ArithmeticNode):
        left = evaluate(node.left, variables)
        right = evaluate(node.right, variables)
        return SUPPORTED_OPERATORS[node.operator](left, right)
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
    elif isinstance(node, IfNode):
        condition = evaluate(node.condition, variables)
        if condition:
            for statement in node.body:
                evaluate(statement, variables)
        elif node.else_body:
            for statement in node.else_body:
                evaluate(statement, variables)
    else:
        if node in variables:
            return variables[node]

    # TODO: Should we be setting these back to a nodes?
    return node
