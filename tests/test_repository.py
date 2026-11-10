import io
import tarfile
from unittest.mock import call, patch
from urllib.error import URLError

import pytest

from src.repository import download_index


def make_archive(name="APKINDEX", content=b"P:test\n"):
    buffer = io.BytesIO()

    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        info = tarfile.TarInfo(name)
        info.size = len(content)
        archive.addfile(info, io.BytesIO(content))

    return buffer.getvalue()


def test_download_index():
    archive_data = make_archive()

    with patch(
        "src.repository.urlopen",
        return_value=io.BytesIO(archive_data)
    ) as mocked_urlopen:
        result = download_index("https://example.com/alpine/")

    assert result == "P:test\n"
    assert mocked_urlopen.call_args == call(
        "https://example.com/alpine/APKINDEX.tar.gz",
        timeout=15
    )


def test_missing_index():
    archive_data = make_archive("README", b"test")

    with patch(
        "src.repository.urlopen",
        return_value=io.BytesIO(archive_data)
    ):
        with pytest.raises(ValueError, match="APKINDEX"):
            download_index("https://example.com")


def test_invalid_archive():
    with patch(
        "src.repository.urlopen",
        return_value=io.BytesIO(b"invalid archive")
    ):
        with pytest.raises(ValueError, match="Ошибка чтения"):
            download_index("https://example.com")


def test_network_error():
    with patch(
        "src.repository.urlopen",
        side_effect=URLError("Connection failed")
    ):
        with pytest.raises(ValueError, match="Не удалось скачать"):
            download_index("https://example.com")


def test_timeout():
    with patch(
        "src.repository.urlopen",
        side_effect=TimeoutError("Timeout")
    ):
        with pytest.raises(ValueError, match="Не удалось скачать"):
            download_index("https://example.com")


def test_invalid_encoding():
    archive_data = make_archive(content=b"\xff\xfe")

    with patch(
        "src.repository.urlopen",
        return_value=io.BytesIO(archive_data)
    ):
        with pytest.raises(ValueError, match="Ошибка чтения"):
            download_index("https://example.com")
