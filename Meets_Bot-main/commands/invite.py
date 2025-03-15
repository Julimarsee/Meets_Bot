from telebot.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import logging
from utils.filework import read_text_file
from .Command import Command
from keyboards import YesKeyboardFactory, AcceptKeyboardFactory, RetryKeyboardFactory

class InviteCommand(Command):

    def __init__(self):
        super().__init__()
        self.commands = ['invite']
        self.description = 'Приглашение'
        self.user_data = {}
        self.time = None
        self.place = None
        self.description_text = None
        self.receiver_usernames = []
        self.photo_file_id = None
        self.invite_text = None
        self.receiver_chat_id = None

    def time_choosing(self, message: Message):
        self.bot.telebot.send_message(message.chat.id, read_text_file('Meets_Bot-Main/messages/time.md'))
        self.bot.telebot.register_next_step_handler(message, self.place_choosing)

    def execute_command(self, message: Message):
        chat_id = message.chat.id

        if self.db.check_user_exists(chat_id):
            self.time_choosing(message)
        else:
            self.bot.send_text_file(message, 'Meets_Bot-Main/messages/go.md')

    def place_choosing(self, message: Message, retry=False):
        try:
            chat_id = message.chat.id
            self.time = message.text
            if retry:
                self.bot.telebot.send_message(chat_id, 'Хотите изменить что-то еще?', reply_markup=RetryKeyboardFactory.get('retry'))
                self.bot.telebot.register_next_step_handler(message, self.retry)
            else:
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь введите место встречи:")
                self.bot.telebot.register_next_step_handler(message, self.write_description)

        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка сохранения времени. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.time_choosing)

    def write_description(self, message: Message, retry=False):
        try:
            chat_id = message.chat.id
            self.place = message.text
            if retry:
                self.bot.telebot.send_message(chat_id, 'Хотите изменить что-то еще?', reply_markup=RetryKeyboardFactory.get('retry'))
                self.bot.telebot.register_next_step_handler(message, self.retry)
            else:
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь введите описание встречи:")
                self.bot.telebot.register_next_step_handler(message, self.choose_receiver)

        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка сохранения места. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.time_choosing)

    def choose_receiver(self, message: Message, retry=False):
        try:
            chat_id = message.chat.id
            self.description_text = message.text
            if retry:
                self.bot.telebot.send_message(chat_id, 'Хотите изменить что-то еще?', reply_markup=RetryKeyboardFactory.get('retry'))
                self.bot.telebot.register_next_step_handler(message, self.retry)
            else:
                self.bot.telebot.send_message(chat_id, "Отлично! Теперь введите username приглашаемых через запятую (например, username1, username2):")
                self.bot.telebot.register_next_step_handler(message, self.checking_invite)
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка сохранения описания. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.choose_receiver)

    def checking_invite(self, message: Message, retry=False):
        try:
            chat_id = message.chat.id
            self.receiver_usernames = [username.strip() for username in message.text.split(',')]
            if retry:
                self.bot.telebot.send_message(chat_id, 'Хотите изменить что-то еще?', reply_markup=RetryKeyboardFactory.get('retry'))
                self.bot.telebot.register_next_step_handler(message, self.retry)
            else:
                self.bot.telebot.send_message(chat_id, "Отлично! Вы заполнили приглашение. Хотите добавить фотографию к приглашению?", reply_markup=YesKeyboardFactory.get('yes'))
                self.bot.telebot.register_next_step_handler(message, self.choose_picture)
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка сохранения получателей. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.checking_invite)

    def choose_picture(self, message):
        try:
            chat_id = message.chat.id
            if message.text.lower() == "да":
                self.bot.telebot.send_message(chat_id, "Хорошо, тогда отправьте фотографию:", reply_markup=ReplyKeyboardRemove())
                self.bot.telebot.register_next_step_handler(message, self.send_picture)
            elif message.text.lower() == "нет":
                self.bot.telebot.send_message(chat_id, "Хорошо, тогда сверим результат:", reply_markup=ReplyKeyboardRemove())
                self.show_final_invite(message)
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.choose_picture)

    def send_picture(self, message: Message, retry=False):
        try:
            chat_id = message.chat.id
            self.photo_file_id = message.photo[-1].file_id
            if retry:
                self.bot.telebot.send_message(chat_id, 'Хотите изменить что-то еще?', reply_markup=RetryKeyboardFactory.get('retry'))
                self.bot.telebot.register_next_step_handler(message, self.retry)
            else:
                self.show_final_invite(message)

        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка сохранения фото. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.send_picture)

    def show_final_invite(self, message: Message):
        self.invite_text = (
            f"От кого: {self.db.get_user_name_by_id(message.chat.id)}\n"
            f"Кому: {', '.join(self.receiver_usernames)}\n"
            f"Время встречи: {self.time}\n"
            f"Место встречи: {self.place}\n"
            f"Описание: {self.description_text}\n"
        )
        if self.photo_file_id:
            self.bot.telebot.send_photo(message.chat.id, self.photo_file_id, caption="Фото к приглашению")
        self.bot.telebot.send_message(message.chat.id, self.invite_text)
        self.bot.telebot.send_message(message.chat.id, 'Всё ли верно? Отправить приглашение?', reply_markup=YesKeyboardFactory.get('yes'))
        self.bot.telebot.register_next_step_handler(message, self.checking)

    def checking(self, message, retry=False):
        try:
            chat_id = message.chat.id
            if message.text.lower() == 'да':
                self.accepted_users = []
                self.declined_users = []
                for username in self.receiver_usernames:
                    receiver_chat_id = self.db.get_chat_id_by_username(username)
                    if receiver_chat_id:
                        markup = InlineKeyboardMarkup(row_width=2)
                        accept_button = InlineKeyboardButton("Принять", callback_data=f"accept_{username}")
                        decline_button = InlineKeyboardButton("Отказать", callback_data=f"decline_{username}")
                        markup.add(accept_button, decline_button)

                        if self.photo_file_id:
                            self.bot.telebot.send_photo(receiver_chat_id, self.photo_file_id, caption=self.invite_text, reply_markup=markup)
                        else:
                            self.bot.telebot.send_message(receiver_chat_id, self.invite_text, reply_markup=markup)

                        self.bot.telebot.send_message(chat_id, f"Приглашение отправлено пользователю: {username}", reply_markup=ReplyKeyboardRemove())
                    else:
                        self.bot.telebot.send_message(chat_id, f"Пользователь {username} не найден.", reply_markup=ReplyKeyboardRemove())
            elif message.text.lower() == 'нет' and not retry:
                self.bot.telebot.send_message(chat_id, 'Выберите что вас не устраивает для дальнейшего изменения:', reply_markup=RetryKeyboardFactory.get('retry'))
                self.bot.telebot.register_next_step_handler(message, self.retry)
            elif message.text.lower() == 'нет' and retry:
                self.bot.telebot.send_message(chat_id, 'Приглашение не отправлено', reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.checking)

    def retry(self, message):
        try:
            chat_id = message.chat.id
            if message.text.lower() == "изменить время":
                self.bot.telebot.send_message(chat_id, "Напишите новое время:")
                self.bot.telebot.register_next_step_handler(message, self.place_choosing, retry=True)
            elif message.text.lower() == "изменить место":
                self.bot.telebot.send_message(chat_id, "Напишите новое место:")
                self.bot.telebot.register_next_step_handler(message, self.write_description, retry=True)
            elif message.text.lower() == "изменить получателя":
                self.bot.telebot.send_message(chat_id, "Напишите нового получателя")
                self.bot.telebot.register_next_step_handler(message, self.checking_invite, retry=True)
            elif message.text.lower() == "изменить описание":
                self.bot.telebot.send_message(chat_id, "Напишите новое описание:")
                self.bot.telebot.register_next_step_handler(message, self.choose_receiver, retry=True)
            elif message.text.lower() == "изменить/добавить фотографию":
                self.bot.telebot.send_message(chat_id, "Отправьте фотографию:")
                self.bot.telebot.register_next_step_handler(message, self.send_picture, retry=True)
            elif message.text.lower() == "изменить всё":
                self.bot.telebot.register_next_step_handler(message, self.time_choosing)
            elif message.text.lower() == "отмена":
                self.bot.telebot.send_message(chat_id, "Отправить приглашение?", reply_markup=YesKeyboardFactory.get('yes'))
                self.bot.telebot.register_next_step_handler(message, self.checking, retry=True)
        except Exception as e:
            self.bot.telebot.reply_to(message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
            logging.error(f"Ошибка: {e}")
            self.bot.telebot.register_next_step_handler(message, self.checking)

    def accept_invite(self, call):
        try:
            chat_id = call.message.chat.id
            action, username = call.data.split('_')

            logging.info(f"Processing callback data: action={action}, username={username}")

            if action == "accept":
                receiver_chat_id = self.db.get_chat_id_by_username(username)
                if receiver_chat_id:
                    logging.info(f"Sending acceptance to receiver_chat_id={receiver_chat_id}")
                    self.bot.telebot.send_message(receiver_chat_id, "Вы приняли приглашение!")
                    self.bot.telebot.answer_callback_query(call.id, text="Вы приняли приглашение!")

                self.bot.telebot.send_message(chat_id, f"Пользователь {username} принял приглашение.")

            elif action == "decline":
                receiver_chat_id = self.db.get_chat_id_by_username(username)
                if receiver_chat_id:
                    logging.info(f"Sending decline to receiver_chat_id={receiver_chat_id}")
                    self.bot.telebot.send_message(receiver_chat_id, "Вы отклонили приглашение.")
                    self.bot.telebot.answer_callback_query(call.id, text="Вы отклонили приглашение.")

                self.bot.telebot.send_message(chat_id, f"Пользователь {username} отклонил приглашение.")

        except Exception as e:
            logging.error(f"Error in accept_invite: {e}")
            self.bot.telebot.reply_to(call.message, 'Произошла ошибка. Пожалуйста, попробуйте снова.')
