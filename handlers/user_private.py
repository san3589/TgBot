from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.strategy import FSMStrategy

import keyboards.reply
from filters.chat_types import ChatTypeFilter
from keyboards.reply import kb_tarrifs

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    await message.answer("Добро пожаловать на курс «Научись медитировать с Аджаном Хубертом» 🙏🏻🌿")
    await message.answer("Пожалуйста, введите Ваше Имя и Фамилию: ")


@user_private_router.message(F.text)
async def get_email(message: types.Message):
    await message.answer("Благодарим. Введите Ваш e-mail: ")


@user_private_router.message(F.text)
async def get_vars(message: types.Message):
    await message.answer("Выберите вариант курса: ", reply_markup=kb_tarrifs)


@user_private_router.message(F.text)
async def get_check(message: types.Message):
    await message.answer("""Благодарим за регистрацию🙏🏻\n 
    Вы выбрали курс: \nПожалуйста, произведите оплату по следующим реквизитам: \n
    Номер карты (Сбербанк): 2202208015739585 \n
    Имя: Елена Александровна Е.\n
    После оплаты, пожалуйста, пришлите чек""", reply_markup=keyboards.reply.delkb)


@user_private_router.message(F.photo)
async def get_info(message: types.Message):
    pass




