"""mal core functions"""

import itertools

import printer
import reader
import maltypes

ns = {
    "*": lambda a, b: a * b,
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "/": lambda a, b: a // b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "=": lambda a, b: a == b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "concat": lambda *lists: list(itertools.chain(*lists)),
    "cons": lambda first, rest: [first, *rest],
    "count": lambda expr: len(expr) if expr is not None else 0,
    "empty?": lambda expr: len(expr) == 0,
    "list": lambda *args: list(args),
    "list?": lambda expr: isinstance(expr, list),
    "pr-str": lambda *exprs: " ".join(printer.pr_str(expr, True) for expr in exprs),
    "println": lambda *exprs: print(
        " ".join(printer.pr_str(expr, False) for expr in exprs)
    ),
    "prn": lambda *exprs: print(" ".join(printer.pr_str(expr, True) for expr in exprs)),
    "read-string": reader.read_str,
    "slurp": lambda path: open(path).read(),
    "str": lambda *exprs: "".join(printer.pr_str(expr, False) for expr in exprs),
    "vec": lambda arg: arg
    if isinstance(arg, maltypes.Vector)
    else maltypes.Vector(arg),
}

# atom functions
ns.update(
    {
        "atom": lambda expr: maltypes.Atom(expr),
        "atom?": lambda expr: isinstance(expr, maltypes.Atom),
        "deref": lambda expr: expr.value,
        "reset!": lambda atom, value: atom.reset(value),
        "swap!": lambda atom, func, *args: atom.swap(func, *args),
    }
)
