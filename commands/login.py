from telebot.types import Message
from .Command import Command

class LoginCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['login']
        self.description = 'Регистрация'
        self.user_data = {}  

    def execute_command(self, message: Message):
        self.bot.send_text_file(message, 'messages/login.md')
        self.bot.send_text_file(message, 'messages/name_ask.md')
        
        self.bot.telebot.register_next_step_handler(message, self.process_name_step)

    def process_name_step(self, message: Message):
        try:
            chat_id = message.chat.id
            name = message.text

            if self.db.save_user_name(chat_id, name):
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь введите ваш возраст:")
                self.user_data[chat_id] = {'name': name}
                self.bot.telebot.register_next_step_handler(message, self.process_age_step)
            else:
                self.bot.telebot.send_message(chat_id, "Ошибка при сохранении имени. Попробуйте снова.")
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            print(f"Ошибка: {e}")

    def process_age_step(self, message: Message):
        try:
            chat_id = message.chat.id
            age = int(message.text)

            if self.db.save_user_age(chat_id, age):
                self.user_data[chat_id]['age'] = age
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь введите ваш номер телефона:")
                self.bot.telebot.register_next_step_handler(message, self.process_phone_step)
            else:
                self.bot.telebot.send_message(chat_id, "Ошибка при сохранении возраста. Попробуйте снова.")
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            print(f"Ошибка: {e}")

    def process_phone_step(self, message: Message):
        try:
            chat_id = message.chat.id
            phone = message.text

            if self.db.save_user_phone(chat_id, phone):
                self.user_data[chat_id]['phone'] = phone
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь отправьте ваше местоположение:")
                self.bot.telebot.register_next_step_handler(message, self.process_location_step)
            else:
                self.bot.telebot.send_message(chat_id, "Ошибка при сохранении номера телефона. Попробуйте снова.")
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            print(f"Ошибка: {e}")

    def process_location_step(self, message: Message):
        try:
            chat_id = message.chat.id
            location = message.location

            if self.db.save_user_location(chat_id, location):
                self.user_data[chat_id]['location'] = location
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь выберите ваш пол (М/Ж):")
                self.bot.telebot.register_next_step_handler(message, self.process_gender_step)
            else:
                self.bot.telebot.send_message(chat_id, "Ошибка при сохранении местоположения. Попробуйте снова.")
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            print(f"Ошибка: {e}")

    def process_gender_step(self, message: Message):
        try:
            chat_id = message.chat.id
            gender = message.text.strip().lower()

            if gender in ['м', 'ж']:
                if self.db.save_user_gender(chat_id, gender):
                    self.user_data[chat_id]['gender'] = gender
                    self.bot.telebot.send_message(chat_id, "Отлично! Теперь выберите ваши интересы из списка:")
                    self.bot.telebot.send_message(chat_id, "- \n".join(self.db.interests))
                    self.bot.telebot.register_next_step_handler(message, self.process_interests_step)
                else:
                    self.bot.telebot.send_message(chat_id, "Ошибка при выборе интереса. Попробуйте снова.")
            else:
                self.bot.telebot.send_message(chat_id, "Пожалуйста, введите 'М' или 'Ж'.")
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            print(f"Ошибка: {e}")

    def process_interests_step(self, message: Message):
        try:
            chat_id = message.chat.id
            interests = message.text.split(',') 

            if self.db.save_user_interests(chat_id, interests):
                self.user_data[chat_id]['interests'] = interests
                self.bot.telebot.send_message(chat_id, "Регистрация завершена! Спасибо за предоставленную информацию.")
            else:
                self.bot.telebot.send_message(chat_id, "Ошибка при сохранении интересов. Попробуйте снова.")
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            print(f"Ошибка: {e}")