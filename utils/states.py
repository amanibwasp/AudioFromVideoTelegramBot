from aiogram.dispatcher.filters.state import State, StatesGroup


class FSM(StatesGroup):
    get_href = State()
