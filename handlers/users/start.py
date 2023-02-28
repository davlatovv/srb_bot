from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from keyboards.default import get_main_menu_keyboard
from utils.db_api.db_commands import DBCommands

from loader import dp, _, bot
from data.config import BOT_NICKNAME

db = DBCommands()


@dp.message_handler(CommandStart(), state="*")
async def register_user(message: Message, state: FSMContext):
    if await db.check_ban(message.from_user.id) == False:
        await message.answer(_('Вы заблокированы'), reply_markup=ReplyKeyboardRemove())
    else:
        await state.reset_state()
        languages_markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="🇷🇺 Русский язык",
                    callback_data="lang_ru")],
                [types.InlineKeyboardButton(
                    text="🇺🇿 Ўзбек тили",
                    callback_data="lang_uz")]
            ]
        )
        text = "🇷🇺Для начала выберите удобный вам язык!\n🇺🇿Ўзингизга қулай тилни танланг!"
        user = await db.get_user(message.from_user.id)
        bot_link = f"https://t.me/{BOT_NICKNAME}?start={message.from_user.id}"
        if not user:
            referrer = str(message.get_args())
            if str(referrer) != "":
                if str(referrer) != str(message.from_user.id):
                    await db.add_new_user(ref=referrer, refferal=bot_link)
                    try:
                        await bot.send_message(referrer, _("🔗Благодаря Вашей ссылке, в семье «SRB» новый пользователь🤩"))
                    except Exception as ex:
                        print(ex)
                else:
                    await db.add_new_user(refferal=bot_link)
                    await bot.send_message(message.from_user.id, _("⛔️Вы не можете перейти по собственной ссылке!"))
            else:
                await db.add_new_user(refferal=bot_link)
            await message.answer(text, reply_markup=languages_markup)
        elif not user.photo:
            await state.reset_state()
            await message.answer(text, reply_markup=languages_markup)
        else:
            await message.answer(_("Главное меню"), reply_markup=get_main_menu_keyboard(user.language))


# @dp.callback_query_handler(text_contains="lang")
# async def change_language(call: CallbackQuery):
#     await call.message.edit_reply_markup()
#     lang = call.data[-2:]
#     logging.info(lang)
#     await db.set_language(lang)
#     await call.message.answer(_("Thank you! Lets start to registration. Please enter your name ", locale=lang), reply_markup=get_main_menu_keyboard(lang))
    # await call.message.answer(_("Thank you! Here's our Main Menu", locale=lang))
#














