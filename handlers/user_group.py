from aiogram import Router, types, Bot
from aiogram.filters import Command
from filters.chat_types import ChatTypeFilter, Moderator
from dotenv import find_dotenv
import os
from handlers.public_group import public_group_router

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group']), Moderator(-4108907218))
# user_group_router.include_router(public_group_router)


@user_group_router.message(Command('admin'))
async def get_admin_list(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [member.user.id for member in admins_list if member.status == 'creator' or member.status == 'administrator']
    bot.my_admins_list = admins_list
    bot.chat_id = chat_id
    if message.from_user.id in admins_list:
        os.environ["GROUP_CHAT_ID"] = str(bot.chat_id)

        await message.delete()
