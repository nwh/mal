"""mal step2"""

import ipdb

import reader
import printer
import maltypes


repl_env = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: int(a / b),
}


def READ(src):
    return reader.read_str(src)


def EVAL(ast, env):
    return ast


def PRINT(exp, print_readably=False):
    return printer.pr_str(exp, print_readably)


def rep(src, print_readably=False):
    ast = READ(src)
    exp = EVAL(ast, repl_env)
    return PRINT(exp, print_readably)


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
            pass
        except maltypes.Unbalanced:
            print("unbalanced")
            pass
        except maltypes.NoInput:
            pass


if __name__ == "__main__":
    main()
