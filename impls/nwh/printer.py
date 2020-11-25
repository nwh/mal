"""mal printer"""

import maltypes


def pr_str(ast, print_readably) -> str:

    if isinstance(ast, maltypes.Symbol):
        return ast.name

    if maltypes.is_keyword(ast):
        return ":" + ast[1:]

    if isinstance(ast, str):
        return pr_string(ast, print_readably)

    if ast is maltypes.Nil:
        return "nil"

    if ast is maltypes.MalTrue:
        return "true"

    if ast is maltypes.MalFalse:
        return "false"

    if isinstance(ast, int):
        return str(ast)

    if isinstance(ast, list):
        return "(" + " ".join(pr_str(item, print_readably) for item in ast) + ")"

    if isinstance(ast, maltypes.Vector):
        return "[" + " ".join(pr_str(item, print_readably) for item in ast.items) + "]"

    if isinstance(ast, maltypes.ReaderMap):
        return "{" + " ".join(pr_str(item, print_readably) for item in ast.items) + "}"

    raise ValueError("invalid ast")


def pr_string(ast, print_readably=False):

    if print_readably:
        chars = []
        for ast_char in ast:
            if ast_char == "\n":
                chars.append("\\n")
            elif ast_char == "\\":
                chars.append("\\\\")
            elif ast_char == '"':
                chars.append('\\"')
            else:
                chars.append(ast_char)
        string = "".join(chars)
    else:
        string = ast

    return '"' + string + '"'
