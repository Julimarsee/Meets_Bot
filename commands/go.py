from telebot.types import Message

from .Command import Command

class GoCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['go']
        self.description = 'Включает поиск собеседников'

    def execute_command(self, message: Message):
        chat_id = message.chat.id

        if self.db.check_user_exists(chat_id):
            self.bot.send_text_file(message, 'messages/exists.md')
        else:
            self.bot.send_text_file(message, 'messages/go.md')