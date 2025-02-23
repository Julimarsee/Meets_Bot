from telebot.types import Message
import logging
from .Command import Command
import random
from keyboards import ChooseKeyboardFactory, YesKeyboardFactory, InterestsKeyboardFactory

class GoCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = ['go']
        self.description = 'Включает поиск собеседников'

    def execute_command(self, message: Message, retry=False):
        chat_id = message.chat.id

        if self.db.check_user_exists(chat_id) and not retry:
            self.bot.send_text_file(message, 'messages/exists.md')
            self.bot.telebot.send_message(chat_id, 'Чтобы найти пользователя, выберите интерес для поиска:', reply_markup=InterestsKeyboardFactory.get('interests'))
            self.bot.telebot.register_next_step_handler(message, self.search_people)
        elif not retry:
            self.bot.send_text_file(message, 'messages/go.md')
        else:
            self.bot.telebot.send_message(chat_id, 'Чтобы найти пользователя, выберите интерес для поиска:', reply_markup=InterestsKeyboardFactory.get('interests'))
            self.bot.telebot.register_next_step_handler(message, self.search_people)

    def search_people(self, message: Message):
        try:
            chat_id = message.chat.id
            self.bot.telebot.send_message(chat_id, "Поиск пользователя с заданными интересами")

            current_user = self.db.users.find_one({'chat_id': chat_id})

            matching_users = []
            for interest in current_user['interests']:
                users = self.db.search_users_by_interest(interest)
                matching_users.extend(users)

            matching_users = [user for user in matching_users if user['chat_id'] != chat_id]
            matching_users = list({user['chat_id']: user for user in matching_users}.values())

            if not matching_users:
                self.bot.telebot.send_message(
                    chat_id,
                    "Пользователи с такими интересами не найдены. Хотите продолжить поиск других интересов?",
                    reply_markup=YesKeyboardFactory.get('yes')
                )
                self.bot.telebot.register_next_step_handler(message, self.handle_yes_no_response)
                return

            random_user = random.choice(matching_users)
            user_info = {
                'name': random_user.get('name', 'Не указано'),
                'age': random_user.get('age', 'Не указано'),
                'interests': random_user.get('interests', [])
            }

            response = (
                f"Найден пользователь:\n"
                f"Имя: {user_info['name']}\n"
                f"Возраст: {user_info['age']}\n"
                f"Интересы: {', '.join(user_info['interests'])}"
            )

            self.bot.telebot.send_message(chat_id, response, reply_markup=ChooseKeyboardFactory.get('choose'))

        except Exception as e:
            logging.error(f"Ошибка в search_people: {e}")
            self.bot.telebot.send_message(chat_id, "Произошла ошибка. Пожалуйста, попробуйте снова.")

    def handle_yes_no_response(self, message: Message):
        try:
            chat_id = message.chat.id
            if message.text == 'Да':
                self.execute_command(message, retry=True)
            elif message.text == 'Нет':
                self.bot.telebot.send_message(chat_id, "Поиск завершен.", reply_markup=None)
        except Exception as e:
            logging.error(f"Ошибка в handle_yes_no_response: {e}")
            self.bot.telebot.send_message(chat_id, "Произошла ошибка. Пожалуйста, попробуйте снова.")

    def handle_callback(self, call):
        try:
            chat_id = call.message.chat.id
            data = call.data

            if data.startswith("choose_"):
                target_user_id = int(data.split("_")[1])
                self.send_match_notification(chat_id, target_user_id)
                self.bot.telebot.answer_callback_query(call.id, "Вы выбрали этого пользователя!")
            elif data == "skip":
                self.bot.telebot.answer_callback_query(call.id, "Пользователь пропущен.")
                self.search_people(call.message)
        except Exception as e:
            logging.error(f"Ошибка в handle_callback: {e}")
            self.bot.telebot.answer_callback_query(call.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")

    def send_match_notification(self, user_id: int, target_user_id: int):
        try:
            user = self.db.users.find_one({'chat_id': user_id})
            target_user = self.db.users.find_one({'chat_id': target_user_id})

            if not user or not target_user:
                return

            notification = (
                f"Вас выбрали!\n"
                f"Имя: {user.get('name', 'Не указано')}\n"
                f"Возраст: {user.get('age', 'Не указано')}\n"
                f"Интересы: {', '.join(user.get('interests', []))}"
            )

            self.bot.telebot.send_message(target_user_id, notification)
        except Exception as e:
            logging.error(f"Ошибка при отправке уведомления: {e}")