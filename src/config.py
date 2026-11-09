from pathlib import Path
from urllib.parse import urlparse

import yaml


def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except OSError as error:
        raise ValueError(f"Ошибка открытия конфигурации: {error}")
    except yaml.YAMLError as error:
        raise ValueError(f"Ошибка YAML: {error}")

    if not isinstance(config, dict):
        raise ValueError("Конфигурация должна содержать ключи и значения")

    for key in ("package_name", "version", "repository"):
        value = config.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Некорректный параметр: {key}")

    if not isinstance(config.get("test_mode"), bool):
        raise ValueError("Параметр test_mode должен быть true или false")

    repository = config["repository"]

    if config["test_mode"]:
        if not Path(repository).is_file():
            raise ValueError("Файл тестового репозитория не найден")
    else:
        url = urlparse(repository)
        if url.scheme not in ("http", "https") or not url.netloc:
            raise ValueError("Некорректный URL репозитория")

    return config