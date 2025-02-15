import json
import logging
import os

def is_file_exist(path: str):
    return os.path.exists(path)

def read_text_file(path: str, encoding = 'utf-8'):
    if not is_file_exist(path):
        logging.warning(f"Файла {path} не существует") 
        return ''
    
    with open(path, 'r', encoding=encoding) as file:
        if file.readable():
            return file.read()
        
        logging.warning(f"Файл {path} нечитабелен")
        return ''
    
def parse_json_file(path: str, default = {}):
    if not is_file_exist(path):
        logging.warning(f"Файла {path} не существует")
        return default
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.warning(f"Ошибка при загрузке json файла: {e}")
        return default