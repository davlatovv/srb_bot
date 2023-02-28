from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_language_keyboard(lang):
    language_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇷🇺 Русский")
            ],
            [
                KeyboardButton(text="🇺🇿 Ўзбек тили")
            ],
            [
                KeyboardButton(text=_("🔙 Назад", locale=lang))
            ]
        ],
        resize_keyboard=True
    )

    return language_keyboard
