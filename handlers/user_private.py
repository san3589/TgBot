from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import AiogramError
import os
from dotenv import find_dotenv


import keyboards.reply
from filters.chat_types import ChatTypeFilter
from keyboards.reply import kb_tarrifs

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


class AddLid(StatesGroup):
    name = State()
    email = State()
    type_product = State()
    image = State()


@user_private_router.message(StateFilter(None), CommandStart())
async def start_cmd(message: types.Message, state: FSMContext) -> None:
    await message.answer("Добро пожаловать на курс «Научись медитировать с Аджаном Хубертом» 🙏🏻🌿")
    await message.answer("Пожалуйста, введите Ваше Имя и Фамилию: ")
    await state.set_state(AddLid.name)


@user_private_router.message(AddLid.name, F.text)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Благодарим. Введите Ваш e-mail: ")
    await state.set_state(AddLid.email)


@user_private_router.message(AddLid.email, F.text)
async def get_vars(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Выберите вариант курса: ", reply_markup=kb_tarrifs)
    await state.set_state(AddLid.type_product)


@user_private_router.message(AddLid.type_product, F.text)
async def get_check(message: types, state: FSMContext):
    await state.update_data(type_product=message.text)
    data = await state.get_data()
    await message.answer(f"""Благодарим за регистрацию🙏🏻\n 
    Вы выбрали курс: {data['type_product']}\nПожалуйста, произведите оплату по следующим реквизитам: \n
    Номер карты (Сбербанк): 2202208015739585 \n
    Имя: Елена Александровна Е.\n
    После оплаты, пожалуйста, пришлите чек""", reply_markup=keyboards.reply.delkb)
    await state.set_state(AddLid.image)


@user_private_router.message(AddLid.image, F.photo)
async def get_info(message: types.Message, state:FSMContext, bot:Bot):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer(f"""
Ваша оплата принята 🤍\n

В течение суток на электронную почту придет письмо со ссылкой на вход в GetCourse.\n
Если письма нет, проверьте папку спам.\n
Если не нашли письмо, свяжитесь с координатором курса Еленой: @eliseeva_kines\n

Приятной Вам практики 🙏🏻😌\n
""")
    data_f = await state.get_data()
    group_chat_id = os.getenv("GROUP_CHAT_ID")
    try:
        await bot.send_message(
            chat_id=group_chat_id,
            text=f"Новая заявка: \n"
                 f"Имя пользователя {data_f['name']}\n"
                 f"E-mail: {data_f['email']}\n"
                 f"Вариант курса: {data_f['type_product']}\n"
                 "Чек:"
            ,

            parse_mode='HTML'
        )
        await bot.send_photo(
            chat_id=group_chat_id,
            photo=data_f['image']
        )
    except AiogramError:
        pass
    await state.clear()





