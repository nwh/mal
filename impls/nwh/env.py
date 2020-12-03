"""mal env"""


class Env:
    def __init__(self, outer=None, binds=(), exprs=()):
        self.outer = outer
        self.data = {}

        for idx, symbol in enumerate(binds):
            if symbol.name == "&":
                self.data[binds[idx + 1].name] = list(exprs[idx:])
                break
            self.data[symbol.name] = exprs[idx]

    def __contains__(self, key):
        return self.find(key) is not None

    def __getitem__(self, key):
        return self.get(key)

    def set(self, key, value):
        self.data[key] = value
        return value

    def find(self, key):
        if key in self.data:
            return self
        if self.outer is not None:
            return self.outer.find(key)

    def get(self, key):
        env = self.find(key)
        if env is None:
            raise KeyError(key)
        return env.data[key]
