from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import admins
from keyboards.default import get_main_menu_keyboard
from loader import dp, _
from utils.db_api.db_commands import DBCommands
from data.config import ADMIN_NICK

db = DBCommands()


@dp.message_handler(commands=["admins"], state="*")
async def bot_help(message: types.Message, state: FSMContext):
    await state.reset_state()
    user = await db.get_user(message.from_user.id)
    if user.language == 'ru':
        await message.answer(f"👨‍💻По любым вопросам и жалобам, обращайтесь к тех. поддержке:@{ADMIN_NICK}", reply_markup=get_main_menu_keyboard(user.language))
    else:
        await message.answer(f"👨‍💻Ҳар қандай савол ва шикоятлар бўйича тех поддержкага ёзинг:@{ADMIN_NICK}", reply_markup=get_main_menu_keyboard(user.language))

