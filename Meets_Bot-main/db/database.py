from os import getenv
from pymongo import MongoClient
import random

import logging

from utils import INTERESTS_JSON
from utils.filework import parse_json_file

class Database:
    def __init__(self):
        self.client = MongoClient(getenv('mongo_url'))
        self.db = self.client[getenv('db_name')]
        self.interests = self.load_interests()
        self.users = self.db['users']

    def load_interests(self) -> list[str]:
        return parse_json_file(INTERESTS_JSON, [])

    def save_user_name(self, chat_id: int, name: str, username: str):
        try:
            self.db.users.update_one(
                {'chat_id': chat_id},
                {'$set': {'name': name, 'username': username}},
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

    def search_users_by_interest(self, interest: str):
        try:
            users = list(self.users.find({'interests': interest}))
            return users
        except Exception as e:
            logging.error(f"Ошибка при поиске пользователей: {e}")
            return []

    def get_chat_id_by_username(self, username: str):
        try:
            user = self.db.users.find_one({'username': username})
            if user:
                return user['chat_id']
            else:
                return None
        except Exception as e:
            logging.error(f"Ошибка при получении chat_id по username: {e}")
            return None

    def get_user_name_by_id(self, chat_id: int):
        try:
            user = self.db.users.find_one({'chat_id': chat_id})
            if user and 'username' in user:
                return user['username']
            else:
                return None
        except Exception as e:
            logging.error(f"Ошибка при получении имени пользователя по chat_id: {e}")
            return None
