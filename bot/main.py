from aiogram import Dispatcher, executor, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from fastapi import HTTPException

from app.db.session import async_session
from app.db.models import Product
from app.main import subscribe_product
from bot.consts import TOKEN
from bot.keyboards import get_product_button
from bot.states import ProductStates
from sqlalchemy.future import select

memory = MemoryStorage()
bot = Bot(TOKEN)

dp = Dispatcher(bot=bot, storage=memory)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать! Нажмите «Получить данные по товару», чтобы начать.",
        reply_markup=get_product_button
    )


@dp.message_handler(text="Получить данные по товару")
async def get_info(message: types.Message, state: FSMContext):
    await message.answer("Введите артикул товара:",
                         reply_markup=ReplyKeyboardRemove())
    await ProductStates.waiting_for_artikul.set()


@dp.message_handler(state=ProductStates.waiting_for_artikul)
async def waiting_for_artikul(message: types.Message, state: FSMContext):
    artikul = message.text.strip()
    if not artikul.isdigit():
        await message.answer(
            "Пожалуйста, введите корректный артикул (только числа)."
        )
        return
    artikul = int(artikul)
    async with async_session() as db:
        stmt = select(Product).where(Product.artikul == artikul)
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()
        if product:
            response = (
                f"Информация о товаре:\n"
                f"Название: {product.name}\n"
                f"Цена: {product.price} руб.\n"
                f"Рейтинг: {product.rating}\n"
                f"В наличии: {product.stock} шт."
            )
        else:
            response = (
                f"Товар с артикулом {artikul} не найден в базе данных. "
                f"Пожалуйста, проверьте корректность артикула или повторите запрос позже."
            )

    # Отправляем пользователю ответ
    await message.answer(response, reply_markup=get_product_button)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
