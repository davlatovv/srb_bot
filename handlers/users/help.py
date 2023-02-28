from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import admins
from keyboards.default import get_main_menu_keyboard
from loader import dp, _
from utils.db_api.db_commands import DBCommands

db = DBCommands()


@dp.message_handler(commands=["admins"], state="*")
async def bot_help(message: types.Message, state: FSMContext):
    await state.reset_state()
    user = await db.get_user(message.from_user.id)
    await message.answer(_("Связь с админами"), reply_markup=get_main_menu_keyboard(user.language))

