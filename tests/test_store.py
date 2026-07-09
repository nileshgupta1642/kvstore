import unittest

from kvstore.store import DEFAULT_TTL_SECONDS, KVStore
from tests.fakes import FakeRedis


class KVStoreTest(unittest.TestCase):
    def test_set_stores_and_overwrites_value(self):
        store = KVStore(client=FakeRedis())

        self.assertTrue(store.set("theme", "dark"))
        self.assertEqual(store.get("theme"), "dark")

        self.assertTrue(store.set("theme", "light"))
        self.assertEqual(store.get("theme"), "light")

    def test_set_applies_default_ttl(self):
        now = [1000]
        redis_client = FakeRedis(clock=lambda: now[0])
        store = KVStore(client=redis_client)

        self.assertTrue(store.set("theme", "dark"))

        self.assertEqual(
            redis_client.ttl("kvstore:theme"),
            DEFAULT_TTL_SECONDS,
        )

    def test_set_accepts_custom_ttl(self):
        now = [1000]
        redis_client = FakeRedis(clock=lambda: now[0])
        store = KVStore(client=redis_client)

        self.assertTrue(store.set("session", "abc123", ttl=5))

        self.assertEqual(redis_client.ttl("kvstore:session"), 5)
        now[0] += 4
        self.assertEqual(store.get("session"), "abc123")
        now[0] += 1
        self.assertIsNone(store.get("session"))

    def test_get_missing_key_returns_none(self):
        store = KVStore(client=FakeRedis())

        self.assertIsNone(store.get("missing"))

    def test_delete_removes_existing_key_and_returns_value(self):
        store = KVStore(client=FakeRedis())
        store.set("session", "abc123")

        self.assertEqual(store.delete("session"), "abc123")
        self.assertIsNone(store.get("session"))

    def test_delete_missing_key_returns_none(self):
        store = KVStore(client=FakeRedis())

        self.assertIsNone(store.delete("missing"))

    def test_list_keys_returns_current_keys(self):
        store = KVStore(client=FakeRedis())
        store.set("alpha", "1")
        store.set("beta", "2")

        self.assertEqual(store.list_keys(), ["alpha", "beta"])

    def test_list_keys_strips_namespace(self):
        redis_client = FakeRedis()
        redis_client.set("other:gamma", "3")
        store = KVStore(client=redis_client, namespace="kvstore:")
        store.set("alpha", "1")
        store.set("beta", "2")

        self.assertEqual(store.list_keys(), ["alpha", "beta"])


if __name__ == "__main__":
    unittest.main()
