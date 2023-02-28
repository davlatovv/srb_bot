from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from aiogram_broadcaster import MessageBroadcaster, exceptions

from data.config import admins
from loader import dp, bot
from utils.db_api.db_commands import DBCommands

db = DBCommands()

kb = [
        [
            types.KeyboardButton(text="Уведомление всем"),
            types.KeyboardButton(text="Количество юзеров"),
        ],
        [
            types.KeyboardButton(text="Заблокировать юзера"),
            types.KeyboardButton(text="Разблокировать юзера"),
        ],

    ]
keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )


@dp.message_handler(text='admin', user_id=admins)
async def admin_menu(msg: Message):
    await msg.answer('Меню', reply_markup=keyboard)


@dp.message_handler(text='Уведомление всем', user_id=admins)
async def broadcast_command_handler(msg: Message, state: FSMContext):
    await msg.answer('Отправьте любой тип сообщения ')
    await state.set_state('broadcast_text')


@dp.message_handler(state='broadcast_text', content_types=types.ContentTypes.ANY)
async def start_broadcast(msg: Message, state: FSMContext):
    await state.finish()
    users = await db.get_all()
    for user in users:
        await MessageBroadcaster(user.user_id, msg).run()
    await msg.answer('Сообщение отправлено!', reply_markup=keyboard)


@dp.message_handler(text='Заблокировать юзера', user_id=admins)
async def count_user(msg: Message, state: FSMContext):
    await state.set_state('ban')
    await msg.answer("Отправьте user_id пользователя которого хотите заблокировать")


@dp.message_handler(state='ban', user_id=admins)
async def count_user(msg: Message, state: FSMContext):
    await state.finish()
    if msg.text.isdigit():
        await db.ban_unbun(user=int(msg.text), ban=True)
        await bot.send_message(chat_id=int(msg.text), text='Вы заблокированы админами!', reply_markup=ReplyKeyboardRemove())
        await msg.answer('Пользователь заблокирован!', reply_markup=keyboard)
    else:
        await msg.answer('Неправильный формат', reply_markup=keyboard)


@dp.message_handler(text='Разблокировать юзера', user_id=admins)
async def count_user(msg: Message, state: FSMContext):
    await state.set_state('unban')
    await msg.answer("Отправьте user_id пользователя которого хотите разблокировать")


@dp.message_handler(state='unban', user_id=admins)
async def count_user(msg: Message, state: FSMContext):
    await state.finish()
    if msg.text.isdigit():
        await db.ban_unbun(user=int(msg.text), ban=False)
        await bot.send_message(chat_id=int(msg.text), text='Вы разблокированы админами!',
                               reply_markup=ReplyKeyboardRemove())
        await msg.answer('Пользователь разблокирован!', reply_markup=keyboard)
    else:
        await msg.answer('Неправильный формат', reply_markup=keyboard)


@dp.message_handler(text='Количество юзеров', user_id=admins)
async def count_user(msg: Message, state: FSMContext):
    await msg.answer(f"""Всего юзеров: {await db.count_users()}
    """)







