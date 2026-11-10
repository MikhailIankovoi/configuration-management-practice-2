
import io
import tarfile
import unittest
from unittest.mock import patch
from urllib.error import URLError

from src.repository import download_index


class RepositoryTests(unittest.TestCase):
    def make_archive(self, name="APKINDEX", content=b"P:test\n"):
        buffer = io.BytesIO()

        with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
            info = tarfile.TarInfo(name)
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))

        return buffer.getvalue()

    def test_download_index(self):
        archive_data = self.make_archive()

        with patch(
            "src.repository.urlopen",
            return_value=io.BytesIO(archive_data)
        ) as mocked_urlopen:
            result = download_index("https://example.com/alpine/")

        self.assertEqual(result, "P:test\n")
        mocked_urlopen.assert_called_once_with(
            "https://example.com/alpine/APKINDEX.tar.gz",
            timeout=15
        )

    def test_missing_index(self):
        archive_data = self.make_archive("README", b"test")

        with patch(
            "src.repository.urlopen",
            return_value=io.BytesIO(archive_data)
        ):
            with self.assertRaisesRegex(ValueError, "APKINDEX"):
                download_index("https://example.com")

    def test_invalid_archive(self):
        with patch(
            "src.repository.urlopen",
            return_value=io.BytesIO(b"invalid archive")
        ):
            with self.assertRaisesRegex(ValueError, "Ошибка чтения"):
                download_index("https://example.com")

    def test_network_error(self):
        with patch(
            "src.repository.urlopen",
            side_effect=URLError("Connection failed")
        ):
            with self.assertRaisesRegex(ValueError, "Не удалось скачать"):
                download_index("https://example.com")

    def test_timeout(self):
        with patch(
            "src.repository.urlopen",
            side_effect=TimeoutError("Timeout")
        ):
            with self.assertRaisesRegex(ValueError, "Не удалось скачать"):
                download_index("https://example.com")

    def test_invalid_encoding(self):
        archive_data = self.make_archive(content=b"\xff\xfe")

        with patch(
            "src.repository.urlopen",
            return_value=io.BytesIO(archive_data)
        ):
            with self.assertRaisesRegex(ValueError, "Ошибка чтения"):
                download_index("https://example.com")


if __name__ == "__main__":
    unittest.main()
