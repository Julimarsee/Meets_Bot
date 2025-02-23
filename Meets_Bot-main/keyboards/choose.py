from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class ChooseKeyboardFactory:
    keyboards = {
            'choose': ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
                        KeyboardButton("Выбрать"),
                        KeyboardButton("Пропустить"),
                    )
    }

    @staticmethod
    def get(key: str):
        return ChooseKeyboardFactory.keyboards.get(key, None)