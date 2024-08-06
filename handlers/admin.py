from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import adminkb, banword_kb, delkb


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())


class AdminState(StatesGroup):
    first_point = State()
    new_lids_add = State()
    ban_word = State()
    add_ban_word = State()
    look_ban_word = State()
    delete_ban_word = State()
    finish_add = State()
    del_finish = State()


@admin_router.message(StateFilter(None) ,Command('admin'))
async def get_hello_admin(message: types.Message, state: FSMContext):
    # await state.clear()
    await message.answer("Что вы хотите сделать?", reply_markup=adminkb)
    await state.set_state(AdminState.first_point)


@admin_router.message(AdminState.first_point, F.text == "Выгрузка новых заявок")
async def get_lids(message: types.Message, state: FSMContext):
    await message.answer(text="Пока не готово", reply_markup=delkb)
    await state.clear()

@admin_router.message(AdminState.first_point, F.text == "Банворд")
async def banword(message: types.Message, state: FSMContext):
    await message.answer(text="Выберите действие", reply_markup=banword_kb)
    await state.set_state(AdminState.ban_word)

@admin_router.message(AdminState.ban_word, F.text == "Добавить запрещенные слова")
async def handle_add_banword(message: types.Message, state: FSMContext):
    await message.answer(
        text="Пришлите слова через перенос строки, например:\n"
             "Кабан\n"
             "Фазан\n"
             "Выхухоль\n",
        reply_markup=delkb
    )
    await state.set_state(AdminState.finish_add)

@admin_router.message(AdminState.ban_word, F.text == "Посмотреть запрещенные слова")
async def handle_look_banword(message: types.Message, state: FSMContext):
    with open('ban.txt', 'r', encoding='utf-8') as file:
        src = file.readlines()
    await message.answer(text=f"{''.join(src)}", reply_markup=delkb)
    await state.clear()

@admin_router.message(AdminState.ban_word, F.text == "Удалить запрещенные слова")
async def handle_delete_banword(message: types.Message, state: FSMContext):
    await message.answer(text="Напишите слово, которое нужно удалить", reply_markup=delkb)
    await state.set_state(AdminState.del_finish)


@admin_router.message(AdminState.del_finish)
async def finish_delete_banword(message: types.Message, state: FSMContext):
    word_to_delete = message.text.strip()
    deleted = False

    with open('ban.txt', 'r', encoding='utf-8') as file:
        srcs = file.readlines()

    with open('ban.txt', 'w', encoding='utf-8') as file:
        for src in srcs:
            if src.strip() != word_to_delete:
                file.write(src)
            else:
                deleted = True

    if deleted:
        await message.answer(text="Слово удалено")
    else:
        await message.answer(text="Слова не найдены")

    await state.clear()


@admin_router.message(AdminState.finish_add)
async def finish_add(message: types.Message, state: FSMContext):
    with open('ban.txt', 'a', encoding='utf-8') as file:
        file.write(message.text + '\n')
    await message.answer(text='Слова добавлены')
    await state.clear()
