from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_tarrifs = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="БАЗОВЫЙ (самостоятельный) 9000 ₽"),
            ],
        [
            KeyboardButton(text="УГЛУБЛЕННЫЙ (с поддержкой куратора) 19000 ₽")
            ],
            [
            KeyboardButton(text="ПРОДВИНУТЫЙ (с поддержкой Учителя) 39000 ₽")
            ]

    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите тип курса: "
)

delkb = ReplyKeyboardRemove()
adminkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Выгрузка новых заявок")
        ]
    ],
    resize_keyboard=True
)
