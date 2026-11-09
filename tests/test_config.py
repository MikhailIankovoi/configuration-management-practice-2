import tempfile
import unittest
from pathlib import Path

import yaml

from src.config import load_config


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.config_path = Path(self.temp_dir.name) / "config.yaml"
        self.data = {
            "package_name": "busybox",
            "version": "1.37.0-r0",
            "repository": "https://example.com/alpine",
            "test_mode": False
        }

    def write_config(self):
        self.config_path.write_text(
            yaml.safe_dump(self.data), encoding="utf-8"
        )

    def test_valid_config(self):
        self.write_config()
        result = load_config(self.config_path)
        self.assertEqual(result, self.data)

    def test_empty_package_name(self):
        self.data["package_name"] = ""
        self.write_config()

        with self.assertRaisesRegex(ValueError, "package_name"):
            load_config(self.config_path)

    def test_empty_version(self):
        self.data["version"] = ""
        self.write_config()

        with self.assertRaisesRegex(ValueError, "version"):
            load_config(self.config_path)

    def test_invalid_repository(self):
        self.data["repository"] = "wrong_url"
        self.write_config()

        with self.assertRaisesRegex(ValueError, "URL"):
            load_config(self.config_path)

    def test_invalid_test_mode(self):
        self.data["test_mode"] = "false"
        self.write_config()

        with self.assertRaisesRegex(ValueError, "test_mode"):
            load_config(self.config_path)

    def test_missing_config_file(self):
        with self.assertRaisesRegex(ValueError, "Ошибка открытия"):
            load_config(self.config_path)

    def test_invalid_yaml(self):
        self.config_path.write_text(
            "package_name: [", encoding="utf-8"
        )

        with self.assertRaisesRegex(ValueError, "Ошибка YAML"):
            load_config(self.config_path)

    def test_missing_test_repository(self):
        self.data["test_mode"] = True
        self.data["repository"] = str(
            Path(self.temp_dir.name) / "missing.txt"
        )
        self.write_config()

        with self.assertRaisesRegex(ValueError, "не найден"):
            load_config(self.config_path)

    def test_existing_test_repository(self):
        graph_path = Path(self.temp_dir.name) / "graph.txt"
        graph_path.write_text("A: B C", encoding="utf-8")

        self.data["test_mode"] = True
        self.data["repository"] = str(graph_path)
        self.write_config()

        result = load_config(self.config_path)
        self.assertEqual(result["repository"], str(graph_path))


if __name__ == "__main__":
    unittest.main()
