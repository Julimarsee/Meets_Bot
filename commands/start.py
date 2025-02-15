from telebot.types import Message

from .Command import Command
from utils.messagework import send_text_file

class StartCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['start']

    def execute_command(self, message: Message):
        send_text_file(message, self.bot, 'messages/start.md')