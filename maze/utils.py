def read_file(file_name: str) -> str:
    """
    :param file_name: имя файла, который нужно прочитать.
    :return: содержимое файла.
    """

    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()
