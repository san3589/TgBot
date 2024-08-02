import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())
from handlers.admin import admin_router
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router

bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = []

dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
dp.include_router(admin_router)
dp.include_router(user_private_router)
dp.include_router(user_group_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
