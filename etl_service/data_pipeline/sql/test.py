def load_query_from_file(filename):
    """Загрузка SQL запроса из файла."""
    with open(filename, 'r') as file:
        return file.read()


