"""mal printer"""

import maltypes


def pr_str(exp, print_readably) -> str:

    if isinstance(exp, maltypes.Symbol):
        return exp.name

    if maltypes.is_keyword(exp):
        return ":" + exp[1:]

    if isinstance(exp, str):
        return pr_string(exp, print_readably)

    if exp is None:
        return "nil"

    if exp is True:
        return "true"

    if exp is False:
        return "false"

    if isinstance(exp, int):
        return str(exp)

    if isinstance(exp, list):
        return "(" + " ".join(pr_str(item, print_readably) for item in exp) + ")"

    if isinstance(exp, maltypes.Vector):
        return "[" + " ".join(pr_str(item, print_readably) for item in exp.items) + "]"

    if isinstance(exp, maltypes.ReaderMap):
        return "{" + " ".join(pr_str(item, print_readably) for item in exp.items) + "}"

    if isinstance(exp, dict):
        items = []
        for key, val in exp.items():
            items.append(pr_str(key, print_readably))
            items.append(pr_str(val, print_readably))
        return "{" + " ".join(items) + "}"

    if callable(exp) or isinstance(exp, maltypes.MalFunc):
        return "#<function>"

    if isinstance(exp, maltypes.Atom):
        return "(atom " + pr_str(exp.value, print_readably) + ")"

    raise ValueError("invalid exp")


def pr_string(exp, print_readably=False):

    if print_readably:
        chars = []
        for exp_char in exp:
            if exp_char == "\n":
                chars.append("\\n")
            elif exp_char == "\\":
                chars.append("\\\\")
            elif exp_char == '"':
                chars.append('\\"')
            else:
                chars.append(exp_char)
        string = '"' + "".join(chars) + '"'
    else:
        string = exp

    return string
