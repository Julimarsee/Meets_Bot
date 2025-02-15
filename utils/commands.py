from dotenv import dotenv_values
from telebot import TeleBot
from telebot.types import BotCommand

def update_commands(bot: TeleBot, path: str):
    commands: list[BotCommand] = []

    for name, description in dotenv_values(path).items():
        commands.append(BotCommand(name, description))

    bot.set_my_commands(commands, None, 'ru')