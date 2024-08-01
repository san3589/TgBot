from aiogram import Router, types
from aiogram.filters import Command
from filters.chat_types import ChatTypeFilter


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group']))

admins_list = []


@user_group_router.message(Command('admin'))
async def get_admin_list(message: types.Message):
    admins_list.append(message.from_user.id)
    await message.delete()
