from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class InlineKeyboardFactory:
    keyboards = {

    }

    @staticmethod
    def get(key: str):
        return InlineKeyboardFactory.keyboards.get(key, None)