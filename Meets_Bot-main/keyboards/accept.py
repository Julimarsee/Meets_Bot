from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class AcceptKeyboardFactory:
    keyboards = {
            'accept': ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
                        KeyboardButton("Принять"),
                        KeyboardButton("Отказать"),
                    )
    }

    @staticmethod
    def get(key: str):
        return AcceptKeyboardFactory.keyboards.get(key, None)