import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kvstore.store import KVStore


class KVStoreTest(unittest.TestCase):
    def test_set_stores_and_overwrites_value(self):
        store = KVStore()

        self.assertTrue(store.set("theme", "dark"))
        self.assertEqual(store.get("theme"), "dark")

        self.assertTrue(store.set("theme", "light"))
        self.assertEqual(store.get("theme"), "light")

    def test_get_missing_key_returns_none(self):
        store = KVStore()

        self.assertIsNone(store.get("missing"))

    def test_delete_removes_existing_key_and_returns_value(self):
        store = KVStore()
        store.set("session", "abc123")

        self.assertEqual(store.delete("session"), "abc123")
        self.assertIsNone(store.get("session"))

    def test_delete_missing_key_returns_none(self):
        store = KVStore()

        self.assertIsNone(store.delete("missing"))

    def test_list_keys_prints_current_keys(self):
        store = KVStore()
        store.set("alpha", "1")
        store.set("beta", "2")
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            store.list_keys()

        self.assertEqual(stdout.getvalue(), "dict_keys(['alpha', 'beta'])\n")


if __name__ == "__main__":
    unittest.main()
