from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class GenderKeyboardFactory:
    keyboards = {
            'gender': ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
                        KeyboardButton("Мужской"),
                        KeyboardButton("Женский"),
                    )
    }

    @staticmethod
    def get(key: str):
        return GenderKeyboardFactory.keyboards.get(key, None)