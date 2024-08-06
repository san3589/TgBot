from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import AiogramError
import os

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
    await state.clear()
    await message.answer("Добро пожаловать на курс <b>«Научись медитировать с Аджаном Хубертом»</b> 🙏🏻🌿", parse_mode='HTML')
    await message.answer("Пожалуйста, введите Ваше Имя и Фамилию: ", reply_markup=keyboards.reply.delkb)
    await state.set_state(AddLid.name)


@user_private_router.message(AddLid.name, F.text)
async def get_name(message: types.Message, state: FSMContext):
    if message.text != "/start":
        await state.update_data(name=message.text)
        await message.answer("Благодарим. Введите Ваш <b>e-mail: </b>", parse_mode='HTML')
        await state.set_state(AddLid.email)
    else:
        await state.clear()


@user_private_router.message(AddLid.email, F.text)
async def get_vars(message: types.Message, state: FSMContext):
    if message.text != "/start":
        await state.update_data(email=message.text)
        await message.answer("Выберите вариант курса: ", reply_markup=kb_tarrifs)
        await state.set_state(AddLid.type_product)
    else:
        await state.clear()


@user_private_router.message(AddLid.type_product, F.text)
async def get_check(message: types, state: FSMContext):
    if message.text != "/start":
        await state.update_data(type_product=message.text)
        data = await state.get_data()
        await message.answer(f"""Благодарим за регистрацию🙏🏻\n 
        Вы выбрали курс:<b> {data['type_product']}</b>\nПожалуйста, произведите оплату по следующим реквизитам: \n
        Номер карты (Сбербанк): 2202208015739585 \n
        Имя: Елена Александровна Е.\n
        После оплаты, пожалуйста, пришлите чек""", parse_mode='HTML',reply_markup=keyboards.reply.delkb)
        await state.set_state(AddLid.image)
    else:
        await state.clear()


@user_private_router.message(AddLid.image)
async def get_info(message: types.Message, state:FSMContext, bot:Bot):
    if message.text != "/start" and message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        await message.answer(f"""
    <b>Ваша оплата принята </b>🤍\n
    
    В течение суток на электронную почту придет письмо со ссылкой на вход в GetCourse.\n
    Если письма нет, проверьте папку <b>спам</b>.\n
    Если не нашли письмо, свяжитесь с координатором курса Еленой: <b>@eliseeva_kines</b>\n
    
    Приятной Вам практики 🙏🏻😌\n
    """, parse_mode='HTML')
        data_f = await state.get_data()
        group_chat_id = os.getenv("GROUP_CHAT_ID")
        try:
            await bot.send_message(
                chat_id=group_chat_id,
                text=f"<b>Новая заявка:</b> \n"
                     f"<i>Имя пользователя:</i> {data_f['name']}\n"
                     f"<i>E-mail:</i> {data_f['email']}\n"
                     f"<i>Вариант курса:</i> {data_f['type_product']}\n"
                     "<i>Чек:</i>"
                ,

                parse_mode='HTML'
            )
            await bot.send_photo(
                chat_id=group_chat_id,
                photo=data_f['image']
            )
        except AiogramError as ae:
            print(ae)
        await state.clear()
    elif message.text and message.text != "/start":
        await message.answer(text="Необходимо прислать  фото")
        await state.set_state(AddLid.image)
    else:
        await state.clear()






