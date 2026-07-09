import subprocess
import sys
import unittest

from click.testing import CliRunner

import kvstore.cli as cli_module
from kvstore.store import KVStore


class KVStoreCliTest(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        cli_module.store = KVStore()

    def test_set_and_get_value(self):
        set_result = self.runner.invoke(
            cli_module.cli, ["set", "theme", "dark"]
        )
        get_result = self.runner.invoke(
            cli_module.cli, ["get", "theme"]
        )

        self.assertEqual(set_result.exit_code, 0)
        self.assertEqual(set_result.output, "True\n")
        self.assertEqual(get_result.exit_code, 0)
        self.assertEqual(get_result.output, "dark\n")

    def test_get_missing_key_prints_blank_line(self):
        result = self.runner.invoke(cli_module.cli, ["get", "missing"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "\n")

    def test_delete_removes_key_and_prints_deleted_value(self):
        self.runner.invoke(cli_module.cli, ["set", "token", "abc"])
        delete_result = self.runner.invoke(cli_module.cli, ["delete", "token"])
        get_result = self.runner.invoke(cli_module.cli, ["get", "token"])

        self.assertEqual(delete_result.exit_code, 0)
        self.assertEqual(delete_result.output, "abc\n")
        self.assertEqual(get_result.exit_code, 0)
        self.assertEqual(get_result.output, "\n")

    def test_list_keys_prints_current_keys(self):
        self.runner.invoke(cli_module.cli, ["set", "alpha", "1"])
        self.runner.invoke(cli_module.cli, ["set", "beta", "2"])

        result = self.runner.invoke(cli_module.cli, ["list_keys"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "dict_keys(['alpha', 'beta'])\n")

    def test_cli_module_can_be_run(self):
        result = subprocess.run(
            [sys.executable, "-m", "kvstore.cli", "--help"],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Commands:", result.stdout)


if __name__ == "__main__":
    unittest.main()
