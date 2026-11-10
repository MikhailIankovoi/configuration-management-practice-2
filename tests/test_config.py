import pytest
import yaml

from src.config import load_config


def make_config():
    return {
        "package_name": "busybox",
        "version": "1.37.0-r0",
        "repository": "https://example.com/alpine",
        "test_mode": False,
    }


def write_config(path, data):
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def test_valid_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    data = make_config()
    write_config(config_path, data)

    assert load_config(config_path) == data


def test_empty_package_name(tmp_path):
    config_path = tmp_path / "config.yaml"
    data = make_config()
    data["package_name"] = ""
    write_config(config_path, data)

    with pytest.raises(ValueError, match="package_name"):
        load_config(config_path)


def test_empty_version(tmp_path):
    config_path = tmp_path / "config.yaml"
    data = make_config()
    data["version"] = ""
    write_config(config_path, data)

    with pytest.raises(ValueError, match="version"):
        load_config(config_path)


def test_invalid_repository(tmp_path):
    config_path = tmp_path / "config.yaml"
    data = make_config()
    data["repository"] = "wrong_url"
    write_config(config_path, data)

    with pytest.raises(ValueError, match="URL"):
        load_config(config_path)


def test_invalid_test_mode(tmp_path):
    config_path = tmp_path / "config.yaml"
    data = make_config()
    data["test_mode"] = "false"
    write_config(config_path, data)

    with pytest.raises(ValueError, match="test_mode"):
        load_config(config_path)


def test_missing_config_file(tmp_path):
    config_path = tmp_path / "missing.yaml"

    with pytest.raises(ValueError, match="Ошибка открытия"):
        load_config(config_path)


def test_invalid_yaml(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "package_name: [", encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Ошибка YAML"):
        load_config(config_path)


def test_missing_test_repository(tmp_path):
    config_path = tmp_path / "config.yaml"
    data = make_config()
    data["test_mode"] = True
    data["repository"] = str(tmp_path / "missing.txt")
    write_config(config_path, data)

    with pytest.raises(ValueError, match="не найден"):
        load_config(config_path)


def test_existing_test_repository(tmp_path):
    graph_path = tmp_path / "graph.txt"
    graph_path.write_text("A: B C", encoding="utf-8")

    config_path = tmp_path / "config.yaml"
    data = make_config()
    data["test_mode"] = True
    data["repository"] = str(graph_path)
    write_config(config_path, data)

    assert load_config(config_path)["repository"] == str(graph_path)
