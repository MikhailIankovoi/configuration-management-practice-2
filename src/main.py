from pathlib import Path

from config import load_config
from repository import download_index
from apk_index import find_direct_dependencies


def main():
    config_path = Path(__file__).resolve().parent.parent / "config.yaml"

    try:
        config = load_config(config_path)

        if config["test_mode"]:
            print("Тестовый режим будет реализован на этапе 3")
            return

        index_text = download_index(config["repository"])

        dependencies = find_direct_dependencies(
            index_text,
            config["package_name"],
            config["version"]
        )

        print("Пакет:", config["package_name"])
        print("Версия:", config["version"])
        print("Прямые зависимости:")

        if dependencies:
            for dependency in dependencies:
                print("-", dependency)
        else:
            print("Зависимости отсутствуют")

    except ValueError as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
