from typing import Any

from .base import BaseNode


class CatNode(BaseNode):
    """Cat function: cat("hello ", "world")"""

    def __init__(self, args: list[Any], line_number: int):
        super().__init__(line_number)
        self.args = args


class PrintNode(BaseNode):
    """Print function: p(foo)"""

    def __init__(self, value: Any, line_number: int):
        super().__init__(line_number, value)


class SleepNode(BaseNode):
    """Sleep function: sleep(1000)"""

    def __init__(self, duration: Any, line_number: int):
        super().__init__(line_number, duration)
        self.duration = duration
        self.duration = duration
