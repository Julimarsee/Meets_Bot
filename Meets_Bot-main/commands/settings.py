import logging
from telebot.types import Message

from keyboards import ReplyKeyboardFactory
from utils import parse_json_file
from utils import ADMINS_JSON
from .Command import Command
from .login import LoginCommand  
class SettingsCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['settings']
        self.admins: list[str] = parse_json_file(ADMINS_JSON, [])
        self.description = 'Параметры'

    def execute_command(self, message: Message):
        self.bot.send_text_file(message, 'messages/settings.md')

        self.bot.telebot.send_message(message.chat.id, "Выберите действие:", reply_markup=ReplyKeyboardFactory.get('settings'))

        self.bot.telebot.register_next_step_handler(message, self.process_settings_choice)

    def process_settings_choice(self, message: Message):
        try:
            chat_id = message.chat.id
            choice = message.text

            if choice == "Изменить анкету":
                login_command = LoginCommand()
                login_command.bot = self.bot  
                login_command.db = self.db  
                login_command.execute_command(message, skip_existence_check=True)
            elif choice == "Жалоба":
                self.bot.telebot.send_message(chat_id, "Напишите вашу жалобу:", reply_markup=None)
                self.bot.telebot.register_next_step_handler(message, self.process_complaint)
            elif choice == "Удалить анкету":
                if self.db.delete_user(chat_id):
                    self.bot.telebot.send_message(chat_id, "Ваша анкета успешно удалена.", reply_markup=None)
                else:
                    self.bot.telebot.send_message(chat_id, "Ошибка при удалении анкеты. Попробуйте снова.")
            elif choice == "Премиум":
                if self.db.premium_user(chat_id):
                    self.bot.telebot.send_message(chat_id, "Премиум-статус успешно активирован!", reply_markup=None)
                else:
                    self.bot.telebot.send_message(chat_id, "Ошибка при активации премиум-статуса. Попробуйте снова.")
            else:
                self.bot.telebot.send_message(chat_id, "Неизвестная команда. Пожалуйста, выберите действие из списка.")
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")

    def process_complaint(self, message: Message):
        try:
            chat_id = message.chat.id
            complaint_text = message.text
            username = f'@{message.from_user.username}' if message.from_user.username else message.from_user.id

            for id in self.admins:
                self.bot.telebot.send_message(id, f"Жалоба от пользователя {username}:\n{complaint_text}")

            self.bot.telebot.send_message(chat_id, "Ваша жалоба отправлена администратору. Спасибо за обратную связь!", reply_markup=None)
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка при отправке жалобы. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")