from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, PreCheckoutQuery, LabeledPrice

from data.config import PM_TOKEN, daily_amount
from keyboards.default import to_main_menu, get_main_menu_keyboard
from loader import dp, _, bot
from states.states import PaymentStates
from utils.db_api.db_commands import DBCommands

db = DBCommands()


@dp.message_handler(text=["Хочу", "Не хочу"], state="*")
async def one_day(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    # await state.finish()
    await state.reset_state()
    if message.text == "Хочу":
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Одноразовая оплата',
            description='Test Payment Description',
            payload='test_payment',
            provider_token=PM_TOKEN,
            start_parameter='test_payment',
            currency='UZS',
            prices=[
                LabeledPrice(label='Глаз Бога', amount=daily_amount),
            ],
            photo_url="https://i.ibb.co/V9Kw68Q/photo-2023-02-18-16-52-46.jpg",
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False,
        )
        await message.answer(_("🗄Главное меню:"), reply_markup=get_main_menu_keyboard(user.language))
    elif message.text == "Не хочу":
        user = await db.get_user(message.from_user.id)
        await message.answer(_("🗄Главное меню:"), reply_markup=get_main_menu_keyboard(user.language))
    else:
        await message.answer(_("🗄Главное меню:"))


@dp.message_handler(content_types=[ContentType.SUCCESSFUL_PAYMENT], state=PaymentStates.daily)
async def success_payment(message: Message):
    user = await db.get_user(message.from_user.id)
    await db.finance(user_id=user.user_id, full_name=user.full_name, type="День", amount=10000)
    try:
        answer = await db.get_one_answer(user_id=message.from_user.id)
        if answer.other_lang == 'ru':
            await message.answer_photo(photo=answer.other_photo,
                                       caption=f"""📌Пользователь {answer.other_name} отметил Вас под вопросом: {answer.question}""",
                                       )
        if answer.other_lang == 'uz':
            await message.answer_photo(photo=answer.other_photo,
                                       caption=f"""📌Фойдаланувчи  {answer.other_name} сизни савол остида белгилади: {answer.question}""",
                                       )
    except Exception as ex:
        print(ex)
        user = await db.get_user(message.from_user.id)
        await message.answer(_('Что то пошло не так, попробуйте позже'), reply_markup=get_main_menu_keyboard(user.language))
