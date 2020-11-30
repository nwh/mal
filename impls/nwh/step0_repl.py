def READ(src):
    return src


def EVAL(ast, env=None):
    return ast


def PRINT(exp):
    return exp


def rep(src):
    return PRINT(EVAL(READ(src)))


def main():
    while True:
        try:
            src = input("user> ")
            print(rep(src))
        except EOFError:
            break


if __name__ == "__main__":
    main()
