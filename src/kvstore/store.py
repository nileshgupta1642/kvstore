import os

import redis


DEFAULT_REDIS_HOST = os.environ.get("KVSTORE_REDIS_HOST", "localhost")
DEFAULT_REDIS_PORT = int(os.environ.get("KVSTORE_REDIS_PORT", "6379"))
DEFAULT_REDIS_DB = int(os.environ.get("KVSTORE_REDIS_DB", "0"))
DEFAULT_REDIS_NAMESPACE = os.environ.get("KVSTORE_REDIS_NAMESPACE", "kvstore:")
DEFAULT_TTL_SECONDS = 60


class KVStore:
    def __init__(
        self,
        host: str = DEFAULT_REDIS_HOST,
        port: int = DEFAULT_REDIS_PORT,
        db: int = DEFAULT_REDIS_DB,
        namespace: str = DEFAULT_REDIS_NAMESPACE,
        client=None,
    ):
        self.redis = client or redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.namespace = namespace

    def set(self, key: str, val: str, ttl: int = DEFAULT_TTL_SECONDS) -> bool:
        return bool(self.redis.set(self._redis_key(key), val, ex=ttl))

    def get(self, key: str) -> str | None:
        return self.redis.get(self._redis_key(key))

    def delete(self, key: str) -> str | None:
        value = self.get(key)
        if value is None:
            return None

        self.redis.delete(self._redis_key(key))
        return value

    def list_keys(self) -> list[str]:
        return sorted(
            self._public_key(redis_key)
            for redis_key in self.redis.scan_iter(match=f"{self.namespace}*")
        )

    def _redis_key(self, key: str) -> str:
        return f"{self.namespace}{key}"

    def _public_key(self, redis_key: str | bytes) -> str:
        if isinstance(redis_key, bytes):
            redis_key = redis_key.decode()

        if self.namespace and redis_key.startswith(self.namespace):
            return redis_key[len(self.namespace):]
        return redis_key
