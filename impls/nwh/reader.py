"""mal reader"""

import re
from typing import List

import maltypes

TOKENS = re.compile(
    r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""
)


class Reader:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> str:
        if self.pos >= len(self.tokens):
            raise maltypes.EOF
        return self.tokens[self.pos]

    def next(self) -> str:
        if self.pos >= len(self.tokens):
            raise maltypes.EOF
        self.pos += 1
        return self.tokens[self.pos - 1]

    def __repr__(self):
        return f"<Reader :pos {self.pos} :len {len(self.tokens)}>"


def tokenize(src: str) -> List[str]:
    return [
        token for token in TOKENS.findall(src) if token and not token.startswith(";")
    ]


def read_str(src: str):
    tokens = tokenize(src)
    if not tokens:
        raise maltypes.NoInput

    reader = Reader(tokens)

    return read_form(reader)


def read_form(reader: Reader):

    token = reader.peek()

    if token == "(":
        return read_seq(reader, "(", ")")
    if token == "[":
        return read_seq(reader, "[", "]")
    if token == "{":
        return read_seq(reader, "{", "}")
    else:
        return read_atom(reader)


def read_seq(reader: Reader, stok, etok):

    token = reader.next()
    assert token == stok

    forms = []
    while True:

        next_token = reader.peek()
        if next_token == etok:
            reader.next()
            break

        forms.append(read_form(reader))

    if stok == "(":
        return forms

    if stok == "[":
        return maltypes.Vector(forms)

    if stok == "{":
        if len(forms) % 2:
            raise maltypes.Unbalanced("map")
        return maltypes.ReaderMap(forms)

    raise ValueError("invalid sequence token")


def read_atom(reader: Reader):
    token = reader.next()

    if token == "nil":
        return None

    if token == "true":
        return True

    if token == "false":
        return False

    if token.startswith(":"):
        return maltypes.keyword_prefix + token[1:]

    if token.startswith('"'):
        return read_string(token)

    try:
        return int(token)
    except ValueError:
        pass
    return maltypes.Symbol(token)


def read_string(token):
    """Reads a quoted string."""

    if len(token) < 2 or token[-1] != '"':
        raise maltypes.Unbalanced("string", token)

    assert token[0] == '"'

    chars = []
    escaped = False
    for char in token[1:-1]:
        if escaped:
            if char == "n":
                chars.append("\n")
            elif char == "\\":
                chars.append(char)
            elif char == '"':
                chars.append(char)
            else:
                raise maltypes.Unbalanced("escape")
            escaped = False
        elif char == "\\":
            escaped = True
        else:
            chars.append(char)

    if escaped:
        raise maltypes.Unbalanced("escape")

    return "".join(chars)
