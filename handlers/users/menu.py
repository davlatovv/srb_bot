import math
import csv
from typing import Union
from aiogram.utils.exceptions import ChatNotFound

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, PreCheckoutQuery, ReplyKeyboardRemove,  ContentType, ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

from data.config import PM_TOKEN, monthly_amount
from states.states import *
from keyboards.default import get_main_menu_keyboard, to_main_menu, settings
from keyboards.default.menu_keyboards import subscribe, classes, quiz, rating, one_day
from loader import dp, _, bot
from utils.db_api.db_commands import DBCommands
from datetime import datetime

db = DBCommands()

async def csv_data(list):
    with open('data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(list)
    file.close()
@dp.message_handler(text=["⬅️В главное меню", "⬅️Aсосий менюга"])
async def main_menu(message: types.Message):
    if await db.check_ban(message.from_user.id) == False:
        await message.answer(_("❌Вы заблокированы администрацией бота!\n📲Для выяснения причины свяжитесь с тех.поддержкой."), reply_markup=ReplyKeyboardRemove())
    user = await db.get_user(message.from_user.id)
    await message.answer(_("🗄Главное меню:"), reply_markup=get_main_menu_keyboard(user.language))


@dp.message_handler(text=["❓О боте", "❓Бот ҳақида"])
async def send_about(message: types.Message):
    if await db.check_ban(message.from_user.id) == False:
        await message.answer(_("❌Вы заблокированы администрацией бота!\n📲Для выяснения причины свяжитесь с тех.поддержкой."), reply_markup=ReplyKeyboardRemove())
    else:
        user = await db.get_user(message.from_user.id)
        await message.answer(text=_("""Данный бот создан в целях популяризации учеников той или иной школы и в целом для приятного проведения свободного времени🤗 

И он очень прост в использовании: 
1. Регистрируешься📲
2. Указываешь школу и класс📖
3. Проходишь опросы и получаешь огоньки🔥
😌Никаких сложностей!"""))


@dp.message_handler(text=["🔗Пригласить друзей", "🔗Дўстларингизни чақиринг"])
async def send_about(message: types.Message):
    if await db.check_ban(message.from_user.id) == False:
        await message.answer(_("❌Вы заблокированы администрацией бота!\n📲Для выяснения причины свяжитесь с тех.поддержкой."), reply_markup=ReplyKeyboardRemove())
    else:
        user = await db.get_user(message.from_user.id)
        if user.language == 'ru':
            await message.answer(text=f'Ваша ссылка для приглашения{user.referral}')
        if user.language == 'uz':
            await message.answer(text=f'Сизнинг таклифномангиз ҳаволаси{user.referral}')



@dp.message_handler(text=["🏆Рейтинг", "Менинг лайкларим"])
async def send_likest(message: types.Message):
    if await db.check_ban(message.from_user.id) == False:
        await message.answer(_("❌Вы заблокированы администрацией бота!\n📲Для выяснения причины свяжитесь с тех.поддержкой."), reply_markup=ReplyKeyboardRemove())
    else:
        user = await db.get_user(message.from_user.id)
        await message.answer(text=_("🏆Рейтинг"), reply_markup=rating(user.language))

@dp.message_handler(text=["🔥Ваши огоньки", "🔥Сизнинг чирокчалар"])
async def send_likest(message: types.Message):
    user = await db.get_user(message.from_user.id)
    await message.answer(f"<b>{user.like}</b>🔥")


@dp.message_handler(text=["🏆Общий рейтинг", "🏆Умумий рейтинг"])
async def send_likest(message: types.Message):
    users = [max(user) for user in await db.all_rating()]
    user = await db.like(users[0])
    if user.language == 'uz':
        await message.answer_photo(user.photo,
                                   caption=f'👤Тахаллус:{user.nickname}\n👤Исм, фамилия: {user.full_name}\n🗓️Туғилган сана:{user.age}\n🔥{user.like}')
    if user.language == 'ru':
        await message.answer_photo(user.photo,
                               caption=f'👤Ник:{user.nickname}\n👤Имя, фамилия: {user.full_name}\n🗓️Дата рождения:{user.age}\n🔥{user.like}')


@dp.message_handler(text=["🏆Рейтинг школы", "🏆Мактаб рейтинги"])
async def send_likest(message: types.Message):
    user = await db.get_user(message.from_user.id)
    users = [max(user) for user in await db.school_rating(user.school)]
    top = await db.like(users[0])
    if user.language == 'ru':
        await message.answer_photo(top.photo,
                                   caption=f'👤Ник:{top.nickname}\n👤Имя, фамилия: {top.full_name}\n🗓️Дата рождения:{top.age}\n🔥{top.like}')
    else:
        await message.answer_photo(top.photo,
                                   caption=f'👤Тахаллус:{top.nickname}\n👤Исм, фамилия: {top.full_name}\n🗓️Туғилган сана:{top.age}\n🔥{top.like}')


@dp.message_handler(text=["🏆Рейтинг класса", "🏆Синф рейтинги"])
async def send_likest(message: types.Message):
    user = await db.get_user(message.from_user.id)
    users = [max(user) for user in await db.class_rating(school=user.school, clas=user.classroom)]
    top = await db.like(users[0])
    if user.language == 'ru':
        await message.answer_photo(top.photo, caption=f'👤Ник:{top.nickname}\n👤Имя, фамилия: {top.full_name}\n🗓️Дата рождения:{top.age}\n🔥{top.like}')
    else:
        await message.answer_photo(top.photo, caption=f'👤Тахаллус:{top.nickname}\n👤Исм, фамилия: {top.full_name}\n🗓️Туғилган сана:{top.age}\n🔥{top.like}')


@dp.message_handler(text=["👤Изменить анкету", "👤Профилни ўзгартириш"])
async def send_likest(message: types.Message):
    if await db.check_ban(message.from_user.id) == False:
        await message.answer(_("❌Вы заблокированы администрацией бота!\n📲Для выяснения причины свяжитесь с тех.поддержкой."), reply_markup=ReplyKeyboardRemove())
    else:
        user = await db.get_user(message.from_user.id)
        if user.language == 'ru':
            await message.answer_photo(user.photo,
                                       caption=f'👤Ник:{user.nickname}\n👤Имя, фамилия: {user.full_name}\n🗓️Дата рождения:{user.age}\n🔥{user.like}')
        else:
            await message.answer_photo(user.photo,
                                       caption=f'👤Тахаллус:{user.nickname}\n👤Исм, фамилия: {user.full_name}\n🗓️Туғилган сана:{user.age}\n🔥{user.like}')
        await message.answer(text=_('Ваша анкета\n1.Сменить никнейм\n2.Сменить фото\n3.Поменять язык'), reply_markup=(settings(user.language)))

@dp.message_handler(text="1")
async def send_likest(message: types.Message, state: FSMContext):
    await message.answer(_('✒️Введите свой никнейм: (например: trippieredd34)'))
    await Settings.nickname.set()


@dp.message_handler(state=Settings.nickname)
async def send_likest(message: types.Message, state: FSMContext):
    await db.set_nickname(message.text)
    user = await db.get_user(message.from_user.id)
    if user.language == 'ru':
        await message.answer_photo(user.photo, caption=f'👤Ник:{user.nickname}\n👤Имя, фамилия: {user.full_name}\n🗓️Дата рождения:{user.age}\n🔥{user.like}')
    else:
        await message.answer_photo(user.photo, caption=f'👤Тахаллус:{user.nickname}\n👤Исм, фамилия: {user.full_name}\n🗓️Туғилган сана:{user.age}\n🔥{user.like}')
    await state.finish()


@dp.message_handler(text="2")
async def send_likest(message: types.Message, state: FSMContext):
    await message.answer(_('Пришлите фото'))
    await Settings.photo.set()


@dp.message_handler(state=Settings.photo, content_types=types.ContentType.PHOTO)
async def send_likest(message: types.Message, state: FSMContext):
    await db.set_photo(message.photo[-1].file_id)
    user = await db.get_user(message.from_user.id)
    if user.language == 'ru':
        await message.answer_photo(user.photo, caption=f'👤Ник:{user.nickname}\n👤Имя, фамилия: {user.full_name}\n🗓️Дата рождения:{user.age}\n🔥{user.like}')
    else:
        await message.answer_photo(user.photo, caption=f'👤Тахаллус:{user.nickname}\n👤Исм, фамилия: {user.full_name}\n🗓️Туғилган сана:{user.age}\n🔥{user.like}')
    await state.finish()


@dp.message_handler(text="3")
async def send_likest(message: types.Message, state: FSMContext):
    kb = [
        [
            types.KeyboardButton(text="🇷🇺Русский язык"),
            types.KeyboardButton(text="🇺🇿Ўзбек тили")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(_('Выберите язык'), reply_markup=keyboard)
    await Settings.language.set()


@dp.message_handler(state=Settings.language)
async def send_likest(message: types.Message, state: FSMContext):
    if message.text == "🇷🇺Русский язык":
        await db.set_language('ru')
        user = await db.get_user(message.from_user.id)
        await message.answer('Язык успешно сменен', reply_markup=(settings(user.language)))

    if message.text == "🇺🇿Ўзбек тили":
        await db.set_language('uz')
        user = await db.get_user(message.from_user.id)
        await message.answer('Тил озгартирилди', reply_markup=(settings(user.language)))
    await state.finish()


@dp.message_handler(text=["🤑Подписка", "🤑Обуна"])
async def send_likest(message: types.Message):
    if await db.check_ban(message.from_user.id) == False:
        await message.answer(_("❌Вы заблокированы администрацией бота!\n📲Для выяснения причины свяжитесь с тех.поддержкой."), reply_markup=ReplyKeyboardRemove())
    else:
        user = await db.get_user(message.from_user.id)
        await message.answer(text=_("""ℹ️Оформляя подписку «Глаз Бога», Вы действительно приобретаете Божью силу-видеть всё👀 
У Вас появляется возможность видеть информацию обо всех, кто Вас отметил: имя, фамилия и фото профиля👤"""), reply_markup=(subscribe(user.language)))

@dp.message_handler(text=["Получить подписку", "Обуна олинг"])
async def cmd_pay(message: Message):
    user = await db.get_user(message.from_user.id)
    if user.subscribe == True:
        await message.answer(_('👁️Подписка уже оформлена!'))
    else:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Test payment',
            description='Test Payment Description',
            payload='test_payment',
            provider_token=PM_TOKEN,
            start_parameter='test_payment',
            currency='UZS',
            prices=[
                types.LabeledPrice(label='Глаз Бога', amount=monthly_amount),
            ],
            photo_url="https://i.ibb.co/V9Kw68Q/photo-2023-02-18-16-52-46.jpg",
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False,
        )


@dp.message_handler(content_types=[ContentType.SUCCESSFUL_PAYMENT], state=PaymentStates.monthly)
async def success_payment(message: Message):
    user = await db.get_user(message.from_user.id)
    await db.finance(user_id=user.user_id, full_name=user.full_name, type="Месяц", amount=250000)
    now = datetime.now()
    try:
        await db.set_subscribe(True)
        await db.start_premium(now.strftime('%Y-%m-%d %H:%M:%S'))
        user = await db.get_user(message.from_user.id)
        await message.answer(_("""🎉Поздравляю!\n✅Вы успешно приобрели подписку!\nТеперь пользоваться ботом будет еще приятнее🤑"""), reply_markup=get_main_menu_keyboard(user.language))
    except Exception as ex:
        print(ex)
        user = await db.get_user(message.from_user.id)
        await message.answer(_('Что то пошло не так, попробуйте позже'), reply_markup=get_main_menu_keyboard(user.language))


@dp.message_handler(text=["🟢Начать опрос", "🟢Сўровни бошлаш"])
async def begin_quiz(message: Message):
    if await db.check_ban(message.from_user.id) == False:
        await message.answer(_('❌Вы заблокированы администрацией бота!\n\n📲Для выяснения причины свяжитесь с тех.поддержкой.'), reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(_("""👨‍💻Короткое введение: Начав опрос-вы можете отметить кого-угодно из класса который выберете-простым нажатием на кнопку с его именем. Каждому пользователю, после того как вы отметите его-начисляется огонек, а также ему приходит уведомление о том, что его отметили. Соответственно с вами такая же ситуация: Вас отмечают-вы сразу же уведомлены и при покупке подписки, можете сразу посмотреть кто это был👀"""))
        await message.answer(_('✍️Введите номер школы, по ученикам которой хотите пройти опрос:'), reply_markup=ReplyKeyboardRemove())
        await db.set_count_ref()
        await Quiz.school.set()


@dp.message_handler(state=Quiz.school)
async def choice_school(message: Message, state: FSMContext):
    if await db.choice_school(message.text) is not False:
        user = await db.get_user(message.from_user.id)
        await message.answer(_("Выберите класс"), reply_markup=classes(user.language))
        await state.update_data(school=message.text)
        await Quiz.start.set()
    else:
        user = await db.get_user(message.from_user.id)
        await message.answer(_("""🤷Школы под этим номером пока нет в базе.
➕Если хотите добавить, свяжитесь с тех.поддержкой./admins 
🏫А пока пройдём по Вашей школе."""), reply_markup=classes(user.language))
        await state.update_data(school=user.school)
        await Quiz.start.set()


@dp.message_handler(state=Quiz.start, text=["6", "7", "8", "9", "10", "11"])
async def go_class(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    await state.update_data(number=message.text)
    school = await state.get_data()
    reg = [reg.classroom for reg in await db.get_classmates_for_quiz1(school=school['school'], number=message.text) if await db.count_rooms(reg.classroom) is not 0]
    kb = [[types.KeyboardButton(text=reg[i])] for i in range(len(reg))]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    keyboard.add(_('Выбор класса⬅️'))
    if await db.get_classmates_for_quiz1(school=school['school'], number=message.text) == []:
        if user.language == 'ru':
            await message.answer(
                f'⛔️Упс! В вашей школе пока что нет зарегистрированных {message.text}-классников, но вы можете пригласить их по этой ссылке: ({user.referral})',
                reply_markup=classes(user.language))
        if user.language == 'uz':
            await message.answer(
                f'⛔️Вой! Мактабингизда ҳали рўйхатдан ўтган талабалар йўқ {message.text}-синф ўқувчилари, лекин сиз уларни ушбу ҳавола орқали таклиф қилишингиз мумкин: ({user.referral})',
                reply_markup=classes(user.language))
        await Quiz.start.set()
    else:
        await message.answer(f"{message.text} классы из вашей школы", reply_markup=keyboard)
        await state.update_data(step_quest=-1, step_btn=1)
        await Quiz.question.set()


@dp.message_handler(state=Quiz.question)
async def choice(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    question = await state.get_data()
    quest = await db.get_questions(user.language, question['number'])
    try:
        if message.text == "⬅️В главное меню" or message.text == "⬅️Асосий менюга":
            await state.finish()
            user = await db.get_user(message.from_user.id)
            await message.answer(_("🗄Главное меню:"), reply_markup=get_main_menu_keyboard(user.language))
        elif message.text == 'Выбор класса⬅️'or message.text == "Синфни танланг⬅️":
            await message.answer(_("Выберите класс"), reply_markup=classes(user.language))
            await Quiz.start.set()
        elif message.text == '️Далее➡️' or message.text == "Кейингиси➡️":
            await state.update_data(step_btn=int(question['step_btn']) + 1)
            question = await state.get_data()
            reg = [reg.full_name for reg in await db.get_people(question["school"], question['room'])]
            if question['step_btn'] == question['all']:
                await message.answer(quest[int(question['step_quest'])][1], reply_markup=quiz(reg, question['step_btn'], bool=True))
                await Quiz.question.set()
            else:
                await message.answer(quest[int(question['step_quest'])][1], reply_markup=quiz(reg, question['step_btn']))
                await Quiz.question.set()
        elif message.text == 'Назад⬅️' or message.text == "Ортга⬅️":
            await state.update_data(step_btn=int(question['step_btn']) - 1)
            question = await state.get_data()
            reg = [reg.full_name for reg in await db.get_people(question["school"], question['room'])]
            await message.answer(quest[int(question['step_quest'])][1], reply_markup=quiz(reg, question['step_btn']))
            await Quiz.question.set()
        else:
            if message.text.split('"')[0].isdigit():
                await state.update_data(room=message.text)
            question = await state.get_data()
            reg = [reg.full_name for reg in await db.get_people(question["school"], question['room'])]
            digit = [i.isdigit() for i in message.text]
            if not any(digit):
                if await db.get_simple(full_name=message.text) is not None:
                    other = await db.get_user(message.from_user.id)
                    user = await db.get_user(await db.get_simple(full_name=message.text))
                    await db.plus_like(await db.get_simple(full_name=message.text))
                    await db.add_one_subscribe(question=quest[int(question['step_quest'])][1], user_id=user.user_id, other_id=other.user_id, other_photo=other.photo, other_name=other.full_name, other_lang=other.language)
                    if user.language == 'ru':
                        await bot.send_message(
                            text=f"📌Вы были отмечены под вопросом: {quest[int(question['step_quest'])][1]}\n\n🌟Для просмотра личности приобретите подписку «Глаз Бога»👀",
                            chat_id=user.user_id, reply_markup=one_day(user.language))
                    if user.language == 'uz':
                        await bot.send_message(
                            text=f"📌Сиз савол остида белгилангансиз: {quest[int(question['step_quest'])][1]}\n\n🌟Шахсиятни кўриш учун «Худонинг кўзи» обунасини сотиб олинг👀",
                            chat_id=user.user_id)
                else:
                    await db.plus_like(await db.get_premium(full_name=message.text))
                    user = await db.get_user(message.from_user.id)
                    other = await db.get_user(await db.get_premium(full_name=message.text))
                    if other.language == 'ru':
                        await bot.send_photo(chat_id=await db.get_premium(full_name=message.text),
                                             caption=f"""📌Пользователь {user.full_name} отметил Вас под вопросом: {quest[int(question['step_quest'])][1]}""",
                                             photo=user.photo)
                    if other.language == 'uz':
                        await bot.send_photo(chat_id=await db.get_premium(full_name=message.text),
                                             caption=f"""📌Фойдаланувчи  {user.full_name} сизни савол остида белгилади: {quest[int(question['step_quest'])][1]}""",
                                             photo=user.photo)

            await state.update_data(step_quest=str(int(question['step_quest']) + 1), all=math.ceil(len(reg)/4))
            question = await state.get_data()
            await bot.send_message(text=quest[int(question['step_quest'])][1], chat_id=message.chat.id, reply_markup=quiz(reg, question['step_btn']))
            await Quiz.question.set()
    except ChatNotFound:
        await message.answer(_('Этот юзер не пользуется ботом'))
    except Exception as ex:
        print(ex)
        await message.answer(_('✅Опрос успешно пройден!'), reply_markup=get_main_menu_keyboard(user.language))
        await state.finish()






