
class ScenarioContext:
    def __init__(self):
        self._store = {}

    def set(self, key, value):
        self._store[key] = value

    def get(self, key):
        if key not in self._store:
            raise KeyError(f"Context key not found: {key}")
        return self._store[key]

    def has(self, key):
        return key in self._store
