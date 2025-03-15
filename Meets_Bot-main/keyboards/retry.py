from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class RetryKeyboardFactory:
    keyboards = {
        'retry': ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
                        KeyboardButton("Изменить время"),
                        KeyboardButton("Изменить место"),
                        KeyboardButton("Изменить получателя"),
                        KeyboardButton("Изменить описание"),
                        KeyboardButton("Изменить/добавить фотографию"),
                        KeyboardButton("Изменить всё"),
                        KeyboardButton("Отмена")
                    )
    }

    @staticmethod
    def get(key: str):
        return RetryKeyboardFactory.keyboards.get(key, None)