import logging
from telebot.types import Message, ReplyKeyboardRemove
from .Command import Command
from keyboards import GenderKeyboardFactory, InterestsKeyboardFactory 

class LoginCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['login']
        self.description = 'Регистрация'
        self.user_data = {}  

    def execute_command(self, message: Message, skip_existence_check=False):
        chat_id = message.chat.id

        if not skip_existence_check and self.db.check_user_exists(chat_id):
            self.bot.telebot.send_message(chat_id, "Вы уже зарегистрированы")
            return

        self.bot.send_text_file(message, 'Meets_Bot-Main/messages/login.md')
        self.bot.send_text_file(message, 'Meets_Bot-Main/messages/name_ask.md')
        
        self.bot.telebot.register_next_step_handler(message, self.process_name_step)

    def process_name_step(self, message: Message):
        try:
            chat_id = message.chat.id
            name = message.text
            username = message.from_user.username
            if self.db.save_user_name(chat_id, name, username):
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь введите ваш возраст:")
                self.user_data[chat_id] = {'name': name}
                self.bot.telebot.register_next_step_handler(message, self.process_age_step)
            else:
                self.bot.telebot.send_message(chat_id, "Ошибка при сохранении имени. Попробуйте снова.")
                self.bot.telebot.register_next_step_handler(message, self.process_name_step) 
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.process_name_step) 

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
                self.bot.telebot.register_next_step_handler(message, self.process_age_step) 
        except ValueError:
            self.bot.telebot.send_message(chat_id, "Возраст должен быть числом. Пожалуйста, введите возраст еще раз.")
            self.bot.telebot.register_next_step_handler(message, self.process_age_step)  
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.process_age_step)  

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
                self.bot.telebot.register_next_step_handler(message, self.process_phone_step)  
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.process_phone_step) 

    def process_location_step(self, message: Message):
        try:
            chat_id = message.chat.id
            location = message.location

            if self.db.save_user_location(chat_id, location):
                self.user_data[chat_id]['location'] = location
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь выберите ваш пол (м/ж):", reply_markup=GenderKeyboardFactory.get('gender'))
                self.bot.telebot.register_next_step_handler(message, self.process_gender_step)
            else:
                self.bot.telebot.send_message(chat_id, "Ошибка при сохранении местоположения. Попробуйте снова.")
                self.bot.telebot.register_next_step_handler(message, self.process_location_step)  
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.process_location_step)

    def process_gender_step(self, message: Message):
        try:
            chat_id = message.chat.id
            gender = message.text.strip().lower()

            if gender == "женский":
                gender = "ж"
            elif gender == "мужской":
                gender = "м"

            if gender in ['м', 'ж']:
                if self.db.save_user_gender(chat_id, gender):
                    self.user_data[chat_id]['gender'] = gender
                    self.bot.telebot.send_message(chat_id, "Отлично! Теперь выберите ваши интересы из списка:")
                    interests_keyboard = InterestsKeyboardFactory.get('interests')
                    if interests_keyboard:
                        self.bot.telebot.send_message(chat_id, "Выберите интересы:", reply_markup=interests_keyboard)
                        self.bot.telebot.register_next_step_handler(message, self.process_interests_step)
                    else:
                        self.bot.telebot.send_message(chat_id, "Ошибка при загрузке списка интересов.")
                else:
                    self.bot.telebot.send_message(chat_id, "Ошибка при выборе интересов. Попробуйте снова.")
                    self.bot.telebot.register_next_step_handler(message, self.process_gender_step) 
            else:
                self.bot.telebot.send_message(chat_id, "Пожалуйста, введите 'м' или 'ж'.")
                self.bot.telebot.register_next_step_handler(message, self.process_gender_step) 
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.process_gender_step)  

    def process_interests_step(self, message: Message):
        try:
            chat_id = message.chat.id
            user_input = message.text.strip()

            if user_input.lower() == "закончить ввод":
                if self.db.save_user_interests(chat_id, self.user_data[chat_id]['interests']):
                    self.bot.telebot.send_message(chat_id, "Регистрация завершена! Спасибо за предоставленную информацию.", reply_markup=ReplyKeyboardRemove())
                else:
                    self.bot.telebot.send_message(chat_id, "Ошибка при сохранении интересов. Попробуйте снова.")
                return

            if 'interests' not in self.user_data[chat_id]:
                self.user_data[chat_id]['interests'] = []
            self.user_data[chat_id]['interests'].append(user_input)

            self.bot.telebot.send_message(chat_id, "Интерес добавлен. Введите следующий интерес или напишите 'Закончить ввод', чтобы завершить.")
            self.bot.telebot.register_next_step_handler(message, self.process_interests_step)

        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.process_interests_step) 