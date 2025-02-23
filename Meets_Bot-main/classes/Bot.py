import logging
from typing import Callable
from telebot import TeleBot
from telebot.types import BotCommand, Message

from db import Database
from utils.filework import read_text_file

class Bot:
    def __init__(self, token: str):
        self.telebot = TeleBot(token)
        self.db = Database()
        self.commands = []

        self.states: dict[str, Callable[[Message], None]] = {}
        self.current_state: str = None

    def add_commands(self, *commands):
        self.commands.extend(commands)

    def set_state(self, key: str):
        if(self.states.get(key, None)):
            self.current_state = key
            logging.info(f'changed state to "{key}"')
            return True
        else:
            logging.warning(f'state {key} doesnt exist and cant be changed')
            return False

    def add_state(self, key: str, callback: Callable[[Message], None]):
        self.states[key] = callback
    
    def update_state(self, message: Message):
        callback = self.states[self.current_state]
        callback(message)
        logging.info(f'state "{self.current_state}" is updated')

    def set_and_update_state(self, key: str, message: Message):
        if self.set_state(key):
            self.update_state(message)
        else:
            logging.info(f'state "{key}" isnt updated')

    def setup_commands(self):
        for command in self.commands:
            self.add_state(command.name, command.execute_command)
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