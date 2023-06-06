from config import bot
import sys
from aiogram import types


class MessageCollector:
    def __init__(self):
        self.tmp = None
        self.garbage = []
        self.user = None
        self.chat_id = None

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id
        return

    def set_user(self, user):
        self.user = user

    def set_temp_msg(self, message_id):
        self.tmp = message_id

    def add_more(self, message: types.Message):
        self.garbage.append(message.message_id)

    async def delete_msg(self):
        try:
            for message in self.garbage:
                await bot.delete_message(chat_id=self.chat_id, message_id=message)
        except:
            print("Не удалось удалить сообщение по причине")
            print(sys.exc_info())

        self.garbage.clear()

        return

    def clear(self):
        self.user = None
        self.garbage.clear()
        self.tmp = None
        self.chat_id = None
