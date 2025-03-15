from telebot.types import Message

from .Command import Command

class StartCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['start']

    def execute_command(self, message: Message):
        self.bot.send_text_file(message, 'messages/start.md')