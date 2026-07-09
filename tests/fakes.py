from fnmatch import fnmatch


class FakeRedis:
    def __init__(self):
        self.data = {}

    def set(self, name: str, value: str) -> bool:
        self.data[name] = value
        return True

    def get(self, name: str) -> str | None:
        return self.data.get(name)

    def delete(self, *names: str) -> int:
        deleted = 0
        for name in names:
            if name in self.data:
                del self.data[name]
                deleted += 1
        return deleted

    def scan_iter(self, match: str | None = None):
        for key in self.data:
            if match is None or fnmatch(key, match):
                yield key
