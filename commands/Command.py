import logging
from telebot.types import Message

from classes.Bot import Bot
from db.database import Database
from utils.logger import log_receive_message

class Command:
    def __init__(self):
        self.bot: Bot = None
        self.db: Database = None
        
        self.commands = ['']
        self.description: str = None

    @property
    def name(self):
        return self.commands[0] if len(self.commands) > 0 else ''

    def set_bot(self, bot: Bot):
        self.bot = bot

    def set_db(self, db: Database):
        self.db = db

    def setup(self):
        if not self.bot.telebot:
            logging.warning(f'/{self.name} dont setup')
            return
        
        @self.bot.telebot.message_handler(commands=self.commands)
        def command(message: Message):
            log_receive_message(message.text)
            self.execute_command(message)

    def execute_command(self, message: Message):
        pass