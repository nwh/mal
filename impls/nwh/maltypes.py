"""mal types"""

keyword_prefix = "ʞ"


def is_keyword(arg):
    return isinstance(arg, str) and arg.startswith(keyword_prefix)


class Symbol:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Symbol({self.name})"


class Vector:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]

    def __iter__(self):
        return iter(self.items)

    def __eq__(self, other):

        if isinstance(other, Vector):
            return self.items == other.items

        if isinstance(other, list):
            return self.items == other

        return False


class MalFunc:
    def __init__(self, ast, params, env, fn):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn

    def __call__(self, *args):
        return self.fn(*args)


class Atom:
    def __init__(self, value):
        self.value = value

    def reset(self, value):
        self.value = value
        return value

    def swap(self, func, *args):
        self.value = func(self.value, *args)
        return self.value


class ReaderMap:
    def __init__(self, items):
        self.items = items


class MalError(Exception):
    """Mal error."""

    pass


class EOF(MalError):
    """End of file reached."""

    pass


class Unbalanced(MalError):
    """Unbalanced list, vector, map, or string."""

    pass


class NoInput(MalError):
    """Raised when there is no input"""

    pass
