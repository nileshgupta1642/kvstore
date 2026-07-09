import time
from fnmatch import fnmatch


class FakeRedis:
    def __init__(self, clock=None):
        self.clock = clock or time.monotonic
        self.data = {}
        self.expires_at = {}

    def set(self, name: str, value: str, ex: int | None = None) -> bool:
        self.data[name] = value
        if ex is None:
            self.expires_at.pop(name, None)
        else:
            self.expires_at[name] = self.clock() + ex
        return True

    def get(self, name: str) -> str | None:
        self._expire_if_needed(name)
        return self.data.get(name)

    def delete(self, *names: str) -> int:
        deleted = 0
        for name in names:
            self._expire_if_needed(name)
            if name in self.data:
                del self.data[name]
                self.expires_at.pop(name, None)
                deleted += 1
        return deleted

    def scan_iter(self, match: str | None = None):
        for key in list(self.data):
            self._expire_if_needed(key)

        for key in list(self.data):
            if match is None or fnmatch(key, match):
                yield key

    def ttl(self, name: str) -> int:
        self._expire_if_needed(name)
        if name not in self.data:
            return -2

        expires_at = self.expires_at.get(name)
        if expires_at is None:
            return -1

        return max(0, int(expires_at - self.clock()))

    def _expire_if_needed(self, name: str) -> None:
        expires_at = self.expires_at.get(name)
        if expires_at is not None and expires_at <= self.clock():
            self.data.pop(name, None)
            self.expires_at.pop(name, None)
