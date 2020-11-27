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
