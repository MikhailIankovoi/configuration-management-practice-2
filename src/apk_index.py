def find_direct_dependencies(index_text, package_name, version):
    records = index_text.replace("\r\n", "\n").split("\n\n")

    for record in records:
        fields = {}

        for line in record.splitlines():
            key, separator, value = line.partition(":")

            if separator:
                fields[key] = value

        if fields.get("P") != package_name:
            continue

        if fields.get("V") != version:
            continue

        return fields.get("D", "").split()

    raise ValueError(
        f"Пакет {package_name} версии {version} не найден"
    )
