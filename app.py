import asyncio
from _datetime import datetime

import aioschedule as aioschedule
from aiogram.types import PreCheckoutQuery
from aiogram.dispatcher import FSMContext

from data.config import daily_amount, monthly_amount
from loader import bot, _
from states.states import PaymentStates
from utils.db_api.db_commands import DBCommands
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import create_db

db = DBCommands()


async def pre_checkout_query(checout: PreCheckoutQuery, state: FSMContext):
    if checout.total_amount == daily_amount:
        await PaymentStates.daily.set()
        await bot.answer_pre_checkout_query(pre_checkout_query_id=checout.id, ok=True)
    elif checout.total_amount == monthly_amount:
        await PaymentStates.monthly.set()
        await bot.answer_pre_checkout_query(pre_checkout_query_id=checout.id, ok=True)


# async def news():
#     for user in await db.get_all():
#         await bot.send_message(text=_('Уведомление, недели'), chat_id=int(user.user_id))


async def subscribe():
    users = await db.get_all_subscribers()
    for user in users:
        now = datetime.now()
        if now.strftime('%Y-%m-%d') == user.time_end:
            await bot.send_message(chat_id=user.user_id, text=_("Ваша подписка истекла!"))
            await db.set_subscribe2(False, user.user_id)


async def scheduler():
    # aioschedule.every().saturday.at("20:00").do(news)
    aioschedule.every().day.at("03:00").do(subscribe)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    dp.register_pre_checkout_query_handler(pre_checkout_query)
    asyncio.create_task(scheduler())
    import middlewares
    middlewares.setup(dp)

    await set_default_commands(dp)
    await on_startup_notify(dp)

    await create_db()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
