"""mal step0"""


def READ(arg):
    return arg


def EVAL(arg):
    return arg


def PRINT(arg):
    return arg


def rep(arg):
    return PRINT(EVAL(READ(arg)))


def main():
    while True:
        try:
            arg = input("user> ")
            print(rep(arg))
        except EOFError:
            break


if __name__ == "__main__":
    main()
