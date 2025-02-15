def read_file(path: str, encoding = 'utf-8'):
    with open(path, 'r', encoding=encoding) as file:
        if file.readable():
            return file.read()
        return ''