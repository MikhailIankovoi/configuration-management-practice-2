import io
import tarfile
from urllib.error import URLError
from urllib.request import urlopen


def download_index(repository_url):
    index_url = repository_url.rstrip("/") + "/APKINDEX.tar.gz"

    try:
        with urlopen(index_url, timeout=15) as response:
            archive_data = response.read()
    except (URLError, TimeoutError) as error:
        raise ValueError(f"Не удалось скачать индекс: {error}")

    try:
        with tarfile.open(
            fileobj=io.BytesIO(archive_data), mode="r:gz"
        ) as archive:
            index_file = archive.extractfile("APKINDEX")

            if index_file is None:
                raise ValueError("Файл APKINDEX отсутствует")

            with index_file:
                return index_file.read().decode("utf-8")

    except (tarfile.TarError, KeyError, UnicodeDecodeError) as error:
        raise ValueError(f"Ошибка чтения APKINDEX: {error}")