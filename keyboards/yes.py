from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class YesKeyboardFactory:
    keyboards = {
            'yes': ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
                        KeyboardButton("Да"),
                        KeyboardButton("Нет"),
                    )
    }

    @staticmethod
    def get(key: str):
        return YesKeyboardFactory.keyboards.get(key, None)