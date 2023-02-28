import asyncio
from _datetime import datetime

import aioschedule as aioschedule
# from handlers.users.menu import precheckout_query_handler
from loader import bot, _
from utils.db_api.db_commands import DBCommands
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import create_db

db = DBCommands()


async def news():
    for user in await db.get_all():
        await bot.send_message(text=_('Уведомление, недели'), chat_id=int(user.user_id))


async def subscribe():
    users = await db.get_all_subscribers()
    for user in users:
        now = datetime.now()
        if now.strftime('%Y-%m-%d') == user.time_end:
            await bot.send_message(chat_id=user.user_id, text=_("Ваша подписка истекла!"))
            await db.set_subscribe2(False, user.user_id)


async def scheduler():
    aioschedule.every().saturday.at("20:00").do(news)
    aioschedule.every().day.at("03:00").do(subscribe)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())
    # dp.register_pre_checkout_query_handler(precheckout_query_handler)
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    await set_default_commands(dp)
    await on_startup_notify(dp)

    await create_db()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
