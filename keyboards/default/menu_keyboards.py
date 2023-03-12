from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _

def rating(lang):
    rating_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🔥Ваши огоньки", locale=lang)),
                KeyboardButton(text=_("🏆Общий рейтинг", locale=lang)),
            ],
            [
                KeyboardButton(text=_("🏆Рейтинг школы", locale=lang)),
                KeyboardButton(text=_("🏆Рейтинг класса", locale=lang)),
            ],
            [
                KeyboardButton(text=_("⬅️В главное меню", locale=lang)),
            ]
        ],
        resize_keyboard=True
    )
    return rating_kb

def get_main_menu_keyboard(lang):

    main_menu_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🟢Начать опрос", locale=lang)),
                KeyboardButton(text=_("🏆Рейтинг", locale=lang)),
            ],
            [
                KeyboardButton(text=_("👤Изменить анкету", locale=lang)),
                KeyboardButton(text=_("🤑Подписка", locale=lang)),
            ],
            [
                KeyboardButton(text=_("🔗Пригласить друзей", locale=lang)),
                KeyboardButton(text=_("❓О боте", locale=lang)),
            ],

        ],
        resize_keyboard=True
    )

    return main_menu_keyboard


def to_main_menu(lang):
    main = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("⬅️В главное меню", locale=lang)),],
        ], resize_keyboard=True)
    return main


def settings(lang):
    main = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=("1")),
                KeyboardButton(text=("2")),
                KeyboardButton(text=("3")),
            ],
            [
                KeyboardButton(text=_("⬅️В главное меню", locale=lang)),
            ],
        ], resize_keyboard=True)
    return main


def subscribe(lang):
    pay = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("Получить подписку", locale=lang)), ],
            [KeyboardButton(text=_("⬅️В главное меню", locale=lang)), ],
        ], resize_keyboard=True)
    return pay


def classes(lang):
    classess = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=("6")),
                KeyboardButton(text=("7")),
                KeyboardButton(text=("8")),
                KeyboardButton(text=("9")),
                KeyboardButton(text=("10")),
                KeyboardButton(text=("11")),
            ],
        ], resize_keyboard=True)
    return classess

def one_day(lang):
    one = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("Хочу", locale=lang)), ],
            [KeyboardButton(text=_("Не хочу", locale=lang)), ],
        ], resize_keyboard=True)
    return one



def quiz(classmates, num, bool=False):
    people = ReplyKeyboardMarkup(resize_keyboard=True)
    ostatok = len(classmates) % 4
    if len(classmates) <= 4:
        for i in classmates:
            people.add(KeyboardButton(text=i))
        people.add(_("⬅️В главное меню"))
        return people
    elif num == 1:
        for i in classmates[:4]:
            people.add(KeyboardButton(text=i))
        people.add(_('️Далее➡️'))
        people.add(_("⬅️В главное меню"))
        return people
    elif num == 2:
        if len(classmates[4:8]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[4:8]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 3:
        if len(classmates[8:12]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[8:12]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 4:
        if len(classmates[12:16]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[12:16]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 5:
        if len(classmates[16:20]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[16:20]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 6:
        if len(classmates[20:24]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[20:24]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 7:
        if len(classmates[24:28]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[24:28]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 8:
        if len(classmates[28:32]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[28:32]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 9:
        if len(classmates[32:36]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[32:36]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 10:
        if len(classmates[36:40]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[36:40]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 11:
        if len(classmates[40:44]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[40:44]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people
    elif num == 12:
        if len(classmates[44:48]) != 4:
            for i in classmates[-ostatok:]:
                people.add(KeyboardButton(text=i))
            people.add('Назад⬅️')
            people.add(_("⬅️В главное меню"))
            return people
        else:
            for i in classmates[44:48]:
                people.add(KeyboardButton(text=i))
            if ostatok == 0 and bool == True:
                people.add('Назад⬅️')
                people.add(_("⬅️В главное меню"))
            else:
                people.add(KeyboardButton('Назад⬅️'), KeyboardButton('️Далее➡️'))
                people.add(_("⬅️В главное меню"))
            return people




