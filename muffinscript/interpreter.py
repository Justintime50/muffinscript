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
from muffinscript.ast.base import (
    ForLoopNode,
    IfNode,
)
from muffinscript.ast.standard_lib import TypeCheckNode
from muffinscript.ast.types import ListNode
from muffinscript.constants import (
    PYTHON_TO_MUFFIN_TYPES,
    SUPPORTED_OPERATORS,
    SUPPORTED_TYPES,
    UNDEFINED_VARIABLE,
    UNSUPPORTED_STATEMENT,
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
        return variables[node.var_name]
    elif isinstance(node, StringNode):
        if node.value in variables:
            return variables[str(node.value)]
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
    elif isinstance(node, ListNode):
        return [evaluate(item, variables, line_number) for item in node.items]
    elif isinstance(node, ForLoopNode):
        if isinstance(node.iterable, str) and node.iterable in variables:
            iterable = variables[node.iterable]
        else:
            iterable = node.iterable
        if not isinstance(iterable, list):
            raise MuffinScriptRuntimeError(UNSUPPORTED_STATEMENT, line_number)
        results = []
        for item in iterable:
            variables[node.item_name] = item
            for body_line in node.body:
                results.append(evaluate(body_line, variables, line_number))
        return results
    elif isinstance(node, ArithmeticNode):
        left = evaluate(node.left, variables, line_number)
        right = evaluate(node.right, variables, line_number)
        return SUPPORTED_OPERATORS[node.operator](left, right)
    elif isinstance(node, CatNode):
        return "".join([str(evaluate(arg, variables, line_number)) for arg in node.args])
    elif isinstance(node, SleepNode):
        time.sleep(evaluate(node.duration, variables, line_number))  # type: ignore
    elif isinstance(node, TypeCheckNode):
        python_type = type(evaluate(node.value, variables, line_number))
        muffin_type = PYTHON_TO_MUFFIN_TYPES.get(python_type)
        if muffin_type is None:
            raise MuffinScriptBaseError()
        return muffin_type
    elif isinstance(node, IfNode):
        condition = evaluate(node.condition, variables, line_number)
        results = []
        if condition:
            for statement in node.body:
                results.append(evaluate(statement, variables, line_number))
        elif node.else_body:
            for statement in node.else_body:
                results.append(evaluate(statement, variables, line_number))
        return results
    elif node in variables:
        return variables[node]
    elif isinstance(node, str):
        # If we got here, we have an undefined variable
        raise MuffinScriptRuntimeError(UNDEFINED_VARIABLE, line_number)
    else:
        # If we got here, it's a passthrough Python type and we move on
        pass

    return node
