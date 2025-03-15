from dotenv import load_dotenv
from os import getenv

from telebot import TeleBot

from classes.Bot import Bot
from db import Database
from utils import setup_logging
from utils import MAIN_ENV_FILE
from commands import StartCommand, GoCommand, LoginCommand, SettingsCommand, InviteCommand

import logging

def main():
    # prepare

    load_dotenv(MAIN_ENV_FILE)
    setup_logging()

    TOKEN = getenv('token')

    if TOKEN == None: 
        print('no token')
        return
    
    # bot

    bot = Bot(TOKEN)

    bot.add_commands(
        StartCommand(),
        GoCommand(),
        LoginCommand(),
        SettingsCommand(),
        InviteCommand()
    )

    bot.start()

if __name__ == '__main__':
    main()