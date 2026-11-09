from pathlib import Path

from config import load_config


def main():
    config_path = Path(__file__).resolve().parent.parent / "config.yaml"

    try:
        config = load_config(config_path)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    print("Конфигурация визуализатора зависимостей:")
    for key, value in config.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
