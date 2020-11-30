import ipdb

import reader
import printer
import maltypes
import core
from env import Env


def READ(src):
    return reader.read_str(src)


def eval_ast(ast, env: Env):

    if isinstance(ast, maltypes.Symbol):
        # raises KeyError if symbol is not defined
        return env.get(ast.name)

    if isinstance(ast, list):
        return [EVAL(item, env) for item in ast]

    if isinstance(ast, maltypes.Vector):
        return maltypes.Vector([EVAL(item, env) for item in ast.items])

    if isinstance(ast, maltypes.ReaderMap):
        return {
            EVAL(key, env): EVAL(val, env)
            for key, val in zip(ast.items[0::2], ast.items[1::2])
        }

    return ast


def EVAL(ast, env: Env):

    while True:

        if not isinstance(ast, list):
            return eval_ast(ast, env)

        if ast == []:
            return ast

        first, *rest = ast

        if isinstance(first, maltypes.Symbol):

            if first.name == "def!":
                value = EVAL(ast[2], env)
                env.set(ast[1].name, value)
                return value

            if first.name == "let*":
                let_env = Env(outer=env)
                bindings = ast[1]
                if isinstance(bindings, maltypes.Vector):
                    bindings = bindings.items
                for symbol, expr in zip(bindings[0::2], bindings[1::2]):
                    let_env.set(symbol.name, EVAL(expr, let_env))
                env = let_env
                ast = ast[2]
                continue

            if first.name == "do":
                eval_ast(rest[:-1], env)
                ast = rest[-1]
                continue

            if first.name == "if":
                pred = EVAL(rest[0], env)
                if pred is not None and pred is not False:
                    ast = rest[1]
                elif len(rest) > 2:
                    ast = rest[2]
                else:
                    ast = None
                continue

            if first.name == "fn*":
                return maltypes.MalFunc(
                    # function body
                    ast=rest[1],
                    # function parameters
                    params=rest[0],
                    env=env,
                    fn=lambda *exprs: EVAL(
                        rest[1], Env(outer=env, binds=rest[0], exprs=exprs)
                    ),
                )

        # apply function and return
        func, *args = eval_ast(ast, env)

        if isinstance(func, maltypes.MalFunc):
            ast = func.ast
            env = Env(outer=func.env, binds=func.params, exprs=args)
            continue

        if callable(func):
            return func(*args)

        raise maltypes.MalError("not a function", func)


def PRINT(exp, print_readably=False):
    return printer.pr_str(exp, print_readably)


repl_env = Env()
repl_env.data.update(core.ns)


def rep(src, print_readably=False):
    ast = READ(src)
    exp = EVAL(ast, repl_env)
    return PRINT(exp, print_readably)


# define the not function
rep("(def! not (fn* (a) (if a false true)))")


def main():
    while True:
        try:
            src = input("user> ")
            print(rep(src, True))
        except EOFError:
            # input encountered an EOF (ctrl-d)
            break
        except maltypes.EOF:
            print("EOF")
        except maltypes.Unbalanced:
            print("unbalanced")
        except maltypes.NoInput:
            pass
        except KeyError as key_error:
            print(key_error, "not found")


if __name__ == "__main__":
    main()
