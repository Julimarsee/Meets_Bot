from telebot.types import Message

from .Command import Command
from utils.messagework import send_text_file
from db.database import Database

class GoCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['go']
        self.db = Database()

    def execute_command(self, message: Message):
        chat_id = message.chat.id

        if self.db.check_user_exists(chat_id):
            send_text_file(message, self.bot, 'messages/exists.md')
        else:
            send_text_file(message, self.bot, 'message/go.md')