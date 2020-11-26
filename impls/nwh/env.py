"""mal env"""


class Env:
    def __init__(self, outer=None, binds=None, exprs=None):
        self.outer = outer
        self.binds = binds if binds is not None else []
        self.exprs = exprs if exprs is not None else []
        self.data = {}

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
