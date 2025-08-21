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


def evaluate(node: Any, variables: dict[str, SUPPORTED_TYPES], line_number: int) -> SUPPORTED_TYPES:
    """Evaluates tokens to determine what to run."""
    if isinstance(node, PrintNode):
        print(evaluate(node.value, variables, line_number))
    elif isinstance(node, AssignNode):
        variables[node.var_name] = evaluate(node.expression, variables, line_number)
    elif isinstance(node, StringNode):
        # String interpolation
        variables_to_replace = re.findall(r"#\{(.*?)}", str(node.value))
        if variables_to_replace:
            for var in variables_to_replace:
                if var in variables:
                    node.value = str(node.value).replace(f"#{{{var}}}", str(variables[var]))
                else:
                    raise MuffinScriptRuntimeError(UNDEFINED_VARIABLE, line_number)
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
        left = evaluate(node.left, variables, line_number)
        right = evaluate(node.right, variables, line_number)
        return SUPPORTED_OPERATORS[node.operator](left, right)
    elif isinstance(node, CatNode):
        return "".join([arg.value for arg in node.args])
    elif isinstance(node, SleepNode):
        time.sleep(evaluate(node.duration, variables))  # type:ignore
    elif isinstance(node, TypeCheckNode):
        python_type = type(evaluate(node.value, variables, line_number))
        muffin_type = PYTHON_TO_MUFFIN_TYPES.get(python_type)
        if muffin_type is None:
            raise MuffinScriptBaseError()
        return muffin_type
    elif isinstance(node, IfNode):
        condition = evaluate(node.condition, variables, line_number)
        if condition:
            for statement in node.body:
                evaluate(statement, variables, line_number)
        elif node.else_body:
            for statement in node.else_body:
                evaluate(statement, variables, line_number)
    elif node in variables:
        return variables[node]
    elif isinstance(node, str):
        # If we got here, we have an undefined variable
        raise MuffinScriptRuntimeError(UNDEFINED_VARIABLE, line_number)
    else:
        # If we got here, it's a passthrough Python type and we move on
        pass

    return node
