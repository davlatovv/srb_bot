from aiogram.dispatcher.filters.state import StatesGroup, State


class Authorization(StatesGroup):
    full_name = State()
    nickname = State()
    age = State()
    gender = State()
    region = State()
    district = State()
    school = State()
    classroom = State()
    photo = State()
    finish = State()


class Settings(StatesGroup):
    nickname = State()
    photo = State()
    language = State()


class Quiz(StatesGroup):
    question = State()
    answer = State()
    start = State()
    school = State()

