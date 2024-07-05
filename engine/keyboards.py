from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from engine.parser import data


greet_kb = InlineKeyboardBuilder()
greet_kb.add(InlineKeyboardButton(text='Начать', callback_data='start'))

other_kb = InlineKeyboardBuilder()
other_kb.add(InlineKeyboardButton(text='Другое', callback_data='other'))
other_kb.add(InlineKeyboardButton(text='На главную', callback_data='home'))


async def menu():
    keyboard = InlineKeyboardBuilder()
    for i in data['menu']:
        keyboard.add(InlineKeyboardButton(text=str(i), callback_data=str(i)))
    return keyboard.adjust(1).as_markup()


async def keyboard(i):
    keyboard = InlineKeyboardBuilder()
    for i in data['menu'][i]:
        keyboard.add(InlineKeyboardButton(text=str(i), callback_data=str(i)))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='home'))
    return keyboard.adjust(1).as_markup()

#async def menu_obshaga():
#    keyboard = InlineKeyboardBuilder()
#    for i in data['menu']['Общежитие']:
#        if str(i) != 'callback':
#            keyboard.add(InlineKeyboardButton(text=str(i), callback_data='xzpoka'))
#    return keyboard.adjust(1).as_markup()


#async def menu_gruppa():
#    keyboard = InlineKeyboardBuilder()
#    for i in data['menu']['Группа']:
#        if str(i) != 'callback':
#            keyboard.add(InlineKeyboardButton(text=str(i), callback_data='xzzpoka'))
#    return keyboard.adjust(1).as_markup()