from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class ReplyKeyboardFactory:
    keyboards = {
        'settings': ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
                        KeyboardButton("Изменить анкету"),
                        KeyboardButton("Жалоба"),
                        KeyboardButton("Удалить анкету"),
                        KeyboardButton("Премиум")
                    )
    }

    @staticmethod
    def get(key: str):
        return ReplyKeyboardFactory.keyboards.get(key, None)