from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import json

with open('json/interests.json', 'r', encoding='utf-8') as file:
    interests_data = json.load(file)

interests = interests_data['interests']

class InterestsKeyboardFactory:
    @staticmethod
    def get_interests_keyboard():
        keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        for interest in interests:
            keyboard.add(KeyboardButton(interest))

        return keyboard

    @staticmethod
    def get(key: str):
        if key == 'interests':
            return InterestsKeyboardFactory.get_interests_keyboard()
        return None
