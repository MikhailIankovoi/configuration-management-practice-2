import pytest

from src.apk_index import find_direct_dependencies


@pytest.fixture
def index_text():
    return (
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


def test_direct_dependencies(index_text):
    result = find_direct_dependencies(
        index_text, "7zip", "24.09-r0"
    )
    assert result == ["musl", "libgcc", "libstdc++"]


def test_another_package(index_text):
    result = find_direct_dependencies(
        index_text, "busybox", "1.0-r0"
    )
    assert result == ["musl"]


def test_no_dependencies(index_text):
    result = find_direct_dependencies(
        index_text, "empty", "1.0-r0"
    )
    assert result == []


def test_unknown_package(index_text):
    with pytest.raises(ValueError, match="не найден"):
        find_direct_dependencies(
            index_text, "unknown", "1.0-r0"
        )


def test_wrong_version(index_text):
    with pytest.raises(ValueError, match="не найден"):
        find_direct_dependencies(
            index_text, "7zip", "999.0-r0"
        )


def test_windows_line_endings():
    text = "P:7zip\r\nV:24.09-r0\r\nD:musl\r\n"

    result = find_direct_dependencies(
        text, "7zip", "24.09-r0"
    )
    assert result == ["musl"]
