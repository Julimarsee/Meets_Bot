import logging
from telebot import TeleBot
from telebot.types import BotCommand, Message

from db import Database
from utils.filework import read_text_file

class Bot:
    def __init__(self, token: str):
        self.telebot = TeleBot(token)
        self.db = Database()
        self.commands = []

    def add_commands(self, *commands):
        self.commands.extend(commands)

    def setup_commands(self):
        for command in self.commands:
            command.set_bot(self)
            command.set_db(self.db)
            command.setup()

    def update_commands(self):
        commands: list[BotCommand] = []

        for command in self.commands:
            if command.description is None:
                continue
            commands.append(BotCommand(command.name, command.description))

        self.telebot.set_my_commands(commands, None, 'ru')

    def run_bot(self):
        logging.info(f'bot @{self.telebot.user.username} is started!') 
        self.telebot.infinity_polling()

    def send_text_file(self, message: Message, path: str):
        return self.telebot.send_message(message.chat.id, read_text_file(path), parse_mode='Markdown')

    def start(self):
        self.update_commands()
        self.setup_commands()
        self.run_bot()