"""mal core functions"""

from collections import ChainMap

import printer
import maltypes


def prn(expr):
    print(printer.pr_str(expr, True))
    return maltypes.Nil


listq = lambda expr: maltypes.MalTrue if isinstance(expr, list) else maltypes.MalFalse
emptyq = lambda expr: maltypes.MalTrue if len(expr) > 0 else maltypes.MalFalse

ns = ChainMap(
    {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a // b,
        "prn": prn,
        "list": lambda *args: list(args),
        "list?": listq,
        "empty?": emptyq,
        "count": lambda expr: len(expr),
    }
)
