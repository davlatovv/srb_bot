import asyncio
import logging
import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup
from asyncpg import UniqueViolationError

from keyboards.default import get_main_menu_keyboard
from keyboards.default.menu_keyboards import classes
from loader import dp, _, bot
from states.states import Authorization as Auth, Quiz
from utils.db_api.db_commands import DBCommands
from datetime import date

db = DBCommands()


def match_nick(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())


def match_age(age):
    if len(age) == 10:
        re.search("\d\d.\d\d.\d{4}", age)
        return True
    else:
        return False


def calculate_age(birthdate):
    birth = birthdate.split(".")
    birthdate = date(int(birth[-1]), int(birth[1]), int(birth[0]))
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 12:
        return 0
    if age > 18:
        return 1
    return age


def is_cyrrylic(symb):
    return True if u'\u0400' <= symb <=u'\u04FF' or u'\u0500' <= symb <= u'\u052F' else False


@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    lang = call.data[-2:]
    await db.set_language(lang)
    if lang == 'ru':
        await call.message.edit_text("""👋Привет, друг! 
Я Бот-SRB и помогу тебе стать популярнее в школе, а если ты новенький, найти новых друзей🤝
    
Я очень прост в использовании: 
1. Регистрируешься📲
2. Указываешь школу и класс📖
3. Проходишь опросы и получаешь огоньки🔥
😌Никаких сложностей!

🙌Дальше все будет расписано более подробно.
Приятного времяпровождения!😉""")
    else:
        await call.message.edit_text("""👋Салом дўстим!
Мен SRB ботиман ва сизга мактабда машҳур бўлишингизга ёрдам бераман, агар
сиз мактабда янги бўлсангиз, янги дўстлар топинг🤝

Мендан фойдаланиш жуда осон
1. Рўйхатдан ўтинг📲
2. Мактаб ва синфни белгиланг📖
3. Сўровномаларни тўлдиринг ва учқунларни олинг🔥
😌 Қийинчилик йўқ!

🙌Кейинчалик ҳаммаси батафсил баён қилинади.
Вақтингиз яхши ўтсин!😉""")
    await call.message.answer(_("✒️Введите свое имя и фамилию на кириллице: (например:Азизов Азиз)", locale=lang))
    await call.answer(cache_time=1)
    await Auth.full_name.set()


@dp.message_handler(state=Auth.full_name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    if name.isdigit():
        await message.answer(text=_("Пожалуйста введите иимя и фамилию без чисел"))

    elif is_cyrrylic(name) == False:
        await message.answer(text=_("Пожалуйста введите имя и фамилию на кириллице"))

    else:
        await db.set_full_name(name)
        await state.update_data(name=name)
        await message.answer(text=_("✒️Введите свой никнейм: (например: trippieredd34)"))
        await Auth.nickname.set()


@dp.message_handler(state=Auth.nickname)
async def get_surname(message: types.Message, state: FSMContext):
    nickname = message.text
    try:
        await db.set_nickname(nickname)
        await state.update_data(nickname=nickname)
        await message.answer(text=_("🗒Введите свою дату рождения (дд.мм.гггг):"))
        await Auth.age.set()
    except UniqueViolationError:
        await message.answer(text=_("Упс! Данный никнейм уже используется другим пользователем)"))




@dp.message_handler(state=Auth.age)
async def get_age(message: types.Message, state: FSMContext):
    age = message.text
    try:
        if match_age(age) != True:
            await message.answer(text=_("Упс! Кажется вы неверно ввели дату рождения, попробуйте еще раз в таком формате (дд.мм.гггг)"))
        elif calculate_age(age) > 2:
            await db.set_age(age)
            await state.update_data(age=age)
            kb = [
                [
                    types.KeyboardButton(text=_("Мальчик")),
                    types.KeyboardButton(text=_("Девочка"))
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
            await message.answer(text=_("👨🏻👩🏻Укажите свой пол:"), reply_markup=keyboard)
            await Auth.gender.set()
        elif calculate_age(age) == 0:
            await message.answer(text=_("Вам нет полных 12, будем ждать позже"))
        else:
            await message.answer(text=_("Упс! Видимо вы давно окончили школу, и данный бот не для вас"))
    except ValueError:
        await message.answer(text=_("Упс! Кажется вы неверно ввели дату рождения, попробуйте еще раз в таком формате (дд.мм.гггг)"))


@dp.message_handler(state=Auth.gender)
async def get_gender(message: types.Message, state: FSMContext):
    gender = message.text
    user = await db.get_user(message.from_user.id)
    await db.set_gender(gender)
    if gender == "Мальчик" or gender == "Девочка" or gender == "Қиз" or gender == "Йигит":
        await state.update_data(gender=gender)
        reg = [reg.name for reg in await db.get_regions(user.language)]
        kb = [[types.KeyboardButton(text=reg[i])] for i in range(len(reg)) if i != 14]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
        )
        await message.answer(text=_("🗺Укажите свою область:"), reply_markup=keyboard)
        await Auth.region.set()
    else:
        await message.answer(text=_("📌Используйте кнопки, чтобы управлять ботом👇"))


@dp.message_handler(state=Auth.region)
async def get_region(message: types.Message, state: FSMContext):
    region = message.text
    await db.set_region(region)
    await state.update_data(region=region)
    dist = [dist.name for dist in await db.get_district(region)]
    kb = [[types.KeyboardButton(text=dist[i])] for i in range(len(dist))]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(text=_("🌆Укажите город или район:"), reply_markup=keyboard)
    await Auth.district.set()


@dp.message_handler(state=Auth.district)
async def get_district(message: types.Message, state: FSMContext):
    district = message.text
    await db.set_district(district)
    await state.update_data(district=district)
    school = [school.number for school in await db.get_school(district)]
    kb = [[types.KeyboardButton(text=school[i])] for i in range(len(school))]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(text=_("🏢Укажите номер своей школы:"), reply_markup=keyboard)
    await Auth.school.set()


@dp.message_handler(state=Auth.school)
async def get_school(message: types.Message, state: FSMContext):
    school = message.text
    await db.set_school(school)
    await state.update_data(school=school)
    clas = [clas.number for clas in await db.get_classroom(school)]
    kb = [[types.KeyboardButton(text=clas[i])] for i in range(len(clas))]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(text=_("🏛Укажите свой класс:"), reply_markup=keyboard)
    await Auth.classroom.set()


@dp.message_handler(state=Auth.classroom)
async def get_classroom(message: types.Message, state: FSMContext):
    classroom = message.text
    await state.update_data(classroom=classroom)
    await db.set_classroom(classroom)
    await message.answer(_('🖼Добавьте свое фото:'),reply_markup=ReplyKeyboardRemove())
    await Auth.photo.set()


@dp.message_handler(state=Auth.photo, content_types=types.ContentType.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    try:
        photo = message.photo[-1].file_id
        await state.update_data(photo=photo)
        await db.set_photo(photo)
        user = await db.get_user(message.from_user.id)
        repl = ReplyKeyboardMarkup(resize_keyboard=True)
        repl.add(types.KeyboardButton(_('Да')), types.KeyboardButton(_('Нет')))
        await message.answer(_('😉Начинаем опрос?'),reply_markup=repl)
        await Auth.finish.set()
    except:
        await message.answer(_('Что-то пошло не так, попытайтесь снова'))
        await Auth.photo.set()


@dp.message_handler(state=Auth.finish)
async def finish(message: types.Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if message.text == 'Да':
        classroom = await state.get_data()
        if await db.get_classmates(classroom['classroom']) == False:
            if user.language == 'ru':
                await message.answer(f'Упс! В данном классе еще нет зарегистрированных учеников, можете пригласить их по этой ссылке🔗: {user.referral}', reply_markup=get_main_menu_keyboard(lang=user.language))
            if user.language == 'uz':
                await message.answer(f'Вой! Бу синфда ҳали рўйхатдан ўтган талаба йўқ, уларни ушбу ҳавола орқали таклиф қилишингиз мумкин🔗: {user.referral}', reply_markup=get_main_menu_keyboard(lang=user.language))
            await state.finish()
        else:
            user = await db.get_user(message.from_user.id)
            await message.answer(_("Выберите класс"), reply_markup=classes(user.language))
            await Quiz.start.set()
    else:
        await message.answer(_('🗄Главное меню:'), reply_markup=get_main_menu_keyboard(lang=user.language))
        await state.finish()










