from os import getenv
from pymongo import MongoClient

import logging

from utils import INTERESTS_JSON
from utils.filework import parse_json_file

class Database:
    def __init__(self):
        self.client = MongoClient(getenv('mongo_url'))
        self.db = self.client[getenv('db_name')]
        self.interests = self.load_interests()

    def load_interests(self) -> list[str]:
        return parse_json_file(INTERESTS_JSON, [])

    def save_user_name(self, chat_id: int, name: str):
        try:
            self.db.users.update_one(
                {'chat_id': chat_id},
                {'$set': {'name': name}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Ошибка при сохранении имени пользователя: {e}")
            return False

    def save_user_age(self, chat_id: int, age: int):
        try:
            self.db.users.update_one(
                {'chat_id': chat_id},
                {'$set': {'age': age}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Ошибка при сохранении возраста пользователя: {e}")
            return False

    def save_user_phone(self, chat_id: int, phone: str):
        try:
            self.db.users.update_one(
                {'chat_id': chat_id},
                {'$set': {'phone': phone}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Ошибка при сохранении номера телефона: {e}")
            return False

    def save_user_location(self, chat_id: int, location: dict):
        try:
            self.db.users.update_one(
                {'chat_id': chat_id},
                {'$set': {'location': location}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Ошибка при сохранении местоположения: {e}")
            return False

    def save_user_gender(self, chat_id: int, gender: str):
        try:
            self.db.users.update_one(
                {'chat_id': chat_id},
                {'$set': {'gender': gender}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Ошибка при сохранении пола пользователя: {e}")
            return False

    def save_user_interests(self, chat_id: int, interests: list):
        try:
            self.db.users.update_one(
                {'chat_id': chat_id},
                {'$set': {'interests': interests}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Ошибка при сохранении интересов пользователя: {e}")
            return False
        
    def delete_user(self, chat_id: int):
        try:
            result = self.db.users.delete_one({'chat_id': chat_id})
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f"Ошибка при удалении пользователя: {e}")
            return False

    def premium_user(self, chat_id: int):
        try:
            self.db.users.update_one(
                {'chat_id': chat_id},
                {'$set': {'premium': True}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"Ошибка при активации премиум-статуса: {e}")
            return False

    def check_user_exists(self, chat_id: int) -> bool:
        try:
            user = self.db.users.find_one({'chat_id': chat_id})
            return user is not None
        except Exception as e:
            logging.error(f"Ошибка при проверке пользователя: {e}")
            return False