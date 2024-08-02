from aiogram import Router, types, F
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import adminkb


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())


@admin_router.message(Command('admin'))
async def get_hello_admin(message: types.Message):
    await message.answer("Что вы хотите сделать?", reply_markup=adminkb)


@admin_router.message(F.text == "Выгрузка новых заявок")
async def get_lids(message: types.Message):
    pass
