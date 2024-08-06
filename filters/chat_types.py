import os
from aiogram.filters import Filter
from aiogram import types, Bot


class ChatTypeFilter(Filter):

    def __init__(self, chat_types: list[str]):
        self.chat_types = chat_types

    async def __call__(self, message: types.Message):
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message, bot: Bot):
        return message.from_user.id in bot.my_admins_list


class Moderator(Filter):
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.id == self.chat_id



