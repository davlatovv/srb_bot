from aiogram import types

from data.config import admins


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", 'start'),
        types.BotCommand("admins", "Connect to admin")
    ])
