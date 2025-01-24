from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductStates(StatesGroup):
    waiting_for_artikul = State()
