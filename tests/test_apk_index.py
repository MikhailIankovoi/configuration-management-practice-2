import unittest

from src.apk_index import find_direct_dependencies


class ApkIndexTests(unittest.TestCase):
    def setUp(self):
        self.index_text = (
            "P:7zip\n"
            "V:24.09-r0\n"
            "A:x86_64\n"
            "D:musl libgcc libstdc++\n"
            "\n"
            "P:busybox\n"
            "V:1.0-r0\n"
            "A:x86_64\n"
            "D:musl\n"
            "\n"
            "P:empty\n"
            "V:1.0-r0\n"
            "A:x86_64\n"
        )

    def test_direct_dependencies(self):
        result = find_direct_dependencies(
            self.index_text, "7zip", "24.09-r0"
        )
        self.assertEqual(result, ["musl", "libgcc", "libstdc++"])

    def test_another_package(self):
        result = find_direct_dependencies(
            self.index_text, "busybox", "1.0-r0"
        )
        self.assertEqual(result, ["musl"])

    def test_no_dependencies(self):
        result = find_direct_dependencies(
            self.index_text, "empty", "1.0-r0"
        )
        self.assertEqual(result, [])

    def test_unknown_package(self):
        with self.assertRaisesRegex(ValueError, "не найден"):
            find_direct_dependencies(
                self.index_text, "unknown", "1.0-r0"
            )

    def test_wrong_version(self):
        with self.assertRaisesRegex(ValueError, "не найден"):
            find_direct_dependencies(
                self.index_text, "7zip", "999.0-r0"
            )

    def test_windows_line_endings(self):
        text = "P:7zip\r\nV:24.09-r0\r\nD:musl\r\n"

        result = find_direct_dependencies(
            text, "7zip", "24.09-r0"
        )
        self.assertEqual(result, ["musl"])


if __name__ == "__main__":
    unittest.main()
