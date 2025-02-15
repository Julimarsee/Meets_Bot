from telebot import TeleBot
from telebot.types import Message

from utils.logger import log_receive_message

class Command:
    def __init__(self):
        self.bot: TeleBot = None
        self.commands = ['']
    
    def set_bot(self, bot: TeleBot):
        self.bot = bot

    def setup(self):
        if not self.bot: 
            return
        
        @self.bot.message_handler(commands=self.commands)
        def command(message: Message):
            log_receive_message(message.text)
            self.execute_command(message)

    def execute_command(self, message: Message):
        pass