"""mal step4"""

from collections import ChainMap

import ipdb

import reader
import printer
import maltypes
import core


def READ(src):
    return reader.read_str(src)


def eval_ast(ast, env):

    if isinstance(ast, maltypes.Symbol):
        # raises KeyError if symbol is not defined
        return env[ast.name]

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


def EVAL(ast, env):

    while True:
    
        if not isinstance(ast, list):
            return eval_ast(ast, env)
    
        if ast == []:
            return ast
    
        first, *rest = ast
    
        if isinstance(first, maltypes.Symbol):
    
            if first.name == "def!":
                value = EVAL(ast[2], env)
                env[ast[1].name] = value
                return value
    
            if first.name == "let*":
                let_env = env.new_child()
                bindings = ast[1]
                if isinstance(bindings, maltypes.Vector):
                    bindings = bindings.items
                for symbol, expr in zip(bindings[0::2], bindings[1::2]):
                    let_env[symbol.name] = EVAL(expr, let_env)
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
    
                def closure(*exprs):
                    # create new environment and bind parameters
                    fn_args = rest[0]
                    fn_body = rest[1]
    
                    local_binds = {}
                    for idx, symbol in enumerate(fn_args):
                        if symbol.name == "&":
                            local_binds[fn_args[idx + 1].name] = list(exprs[idx:])
                            break
                        local_binds[symbol.name] = exprs[idx]
    
                    fn_env = env.new_child(local_binds)
                    # evaluate the function body
                    return EVAL(fn_body, fn_env)
    
                return closure
    
        # apply function and return
        first, *rest = eval_ast(ast, env)
        return first(*rest)


def PRINT(exp, print_readably=False):
    return printer.pr_str(exp, print_readably)


def rep(src, print_readably=False):
    ast = READ(src)
    exp = EVAL(ast, core.ns)
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
