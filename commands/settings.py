from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from .Command import Command
from utils.messagework import send_text_file
from .login import LoginCommand  
from db.database import Database  

class SettingsCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['settings']
        self.db = Database()  
        self.login_command = LoginCommand()  

    def execute_command(self, message: Message):
        send_text_file(message, self.bot, 'messages/settings.md')

        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        markup.add(
            KeyboardButton("Изменить анкету"),
            KeyboardButton("Жалоба"),
            KeyboardButton("Удалить анкету"),
            KeyboardButton("Премиум")
        )

        self.bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

        self.bot.register_next_step_handler(message, self.process_settings_choice)

    def process_settings_choice(self, message: Message):
        try:
            chat_id = message.chat.id
            choice = message.text

            if choice == "Изменить анкету":
                self.login_command.execute_command(message)
            elif choice == "Жалоба":
                self.bot.send_message(chat_id, "Напишите вашу жалобу:")
                self.bot.register_next_step_handler(message, self.process_complaint)
            elif choice == "Удалить анкету":
                if self.db.delete_user(chat_id):
                    self.bot.send_message(chat_id, "Ваша анкета успешно удалена.")
                else:
                    self.bot.send_message(chat_id, "Ошибка при удалении анкеты. Попробуйте снова.")
            elif choice == "Премиум":
                if self.db.premium_user(chat_id):
                    self.bot.send_message(chat_id, "Премиум-статус успешно активирован!")
                else:
                    self.bot.send_message(chat_id, "Ошибка при активации премиум-статуса. Попробуйте снова.")
            else:
                self.bot.send_message(chat_id, "Неизвестная команда. Пожалуйста, выберите действие из списка.")
        except Exception as e:
            self.bot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            print(f"Ошибка: {e}")

    def process_complaint(self, message: Message):
        try:
            chat_id = message.chat.id
            complaint_text = message.text

            admin_id = "@sherivv"  
            self.bot.send_message(admin_id, f"Жалоба от пользователя {chat_id}:\n{complaint_text}")

            self.bot.send_message(chat_id, "Ваша жалоба отправлена администратору. Спасибо за обратную связь!")
        except Exception as e:
            self.bot.reply_to(message, 'Произошла ошибка при отправке жалобы. Пожалуйста, попробуйте снова.')
            print(f"Ошибка: {e}")