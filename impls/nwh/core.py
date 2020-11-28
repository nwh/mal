"""mal core functions"""

from collections import ChainMap

import printer
import maltypes


ns = ChainMap(
    {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a // b,
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "pr-str": lambda *exprs: " ".join(printer.pr_str(expr, True) for expr in exprs),
        "str": lambda *exprs: "".join(printer.pr_str(expr, False) for expr in exprs),
        "prn": lambda *exprs: print(
            " ".join(printer.pr_str(expr, True) for expr in exprs)
        ),
        "println": lambda *exprs: print(
            " ".join(printer.pr_str(expr, False) for expr in exprs)
        ),
        "list": lambda *args: list(args),
        "list?": lambda expr: isinstance(expr, list),
        "empty?": lambda expr: len(expr) == 0,
        "count": lambda expr: len(expr) if expr is not None else 0,
        "=": lambda a, b: a == b,
    }
)
