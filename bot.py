from dotenv import load_dotenv
from os import getenv

from telebot import TeleBot

from db import Database
from utils import update_commands, setup_logging
from utils import MAIN_ENV_FILE, COMMANDS_ENV_FILE
from commands import StartCommand, GoCommand, LoginCommand, Command

import logging

# prepare

load_dotenv(MAIN_ENV_FILE)
setup_logging()

TOKEN = getenv('token')
bot = TeleBot(TOKEN)

db = Database()

# commands

commands: list[Command] = [
    StartCommand(),
    GoCommand(),
    LoginCommand()
]

for command in commands:
    command.set_bot(bot)
    command.setup()

# main

def main(): 
    if TOKEN == None: 
        return

    update_commands(bot, COMMANDS_ENV_FILE)
    
    logging.info(f'bot @{bot.user.username} is started!') 
    bot.infinity_polling()

if __name__ == '__main__':
    main()