from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from engine.parser import data


greet_kb = InlineKeyboardBuilder()
greet_kb.add(InlineKeyboardButton(text='Начать', callback_data='start'))


other_kb = InlineKeyboardBuilder()
other_kb.add(InlineKeyboardButton(text='Другое', callback_data='other'))
other_kb.add(InlineKeyboardButton(text='На главную', callback_data='home'))


back_kb = InlineKeyboardBuilder()
back_kb.add(InlineKeyboardButton(text='Назад', callback_data='other_back'))


async def menu():
    menu_keyboard = InlineKeyboardBuilder()
    for i, button in enumerate(data['menu']):
        menu_keyboard.add(InlineKeyboardButton(text=str(button), callback_data=str(i)))
    menu_keyboard.add(InlineKeyboardButton(text='Другое', callback_data='other'))
    return menu_keyboard.adjust(1).as_markup()


async def keyboard(enum, buttn):
    cat_keyboard = InlineKeyboardBuilder()  # category
    for i, button in enumerate(data['menu'][buttn]):
        cat_keyboard.add(InlineKeyboardButton(text=str(button), callback_data=str(enum) + "_"+str(i)))
    cat_keyboard.add(InlineKeyboardButton(text='Другое', callback_data='other'))
    cat_keyboard.add(InlineKeyboardButton(text='На главную', callback_data='home'))
    return cat_keyboard.adjust(1).as_markup()
