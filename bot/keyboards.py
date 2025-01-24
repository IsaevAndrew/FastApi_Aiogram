from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_product_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить данные по товару")],
    ],
    resize_keyboard=True
)
