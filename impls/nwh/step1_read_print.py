"""mal step0"""

import ipdb

import reader
import printer
import maltypes


def READ(arg):
    return reader.read_str(arg)


def EVAL(arg):
    return arg


def PRINT(arg, print_readably=False):
    return printer.pr_str(arg, print_readably)


def rep(arg, print_readably=False):
    read_val = READ(arg)
    eval_val = EVAL(read_val)
    return PRINT(eval_val, print_readably)


def main():
    while True:
        try:
            arg = input("user> ")
            print(rep(arg, True))
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
