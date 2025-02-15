from utils.filework import read_file

from telebot import TeleBot
from telebot.types import Message

def send_text_file(message: Message, bot: TeleBot, path: str):
    bot.send_message(message.chat.id, read_file(path), parse_mode='Markdown')