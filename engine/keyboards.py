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
    keyboard = InlineKeyboardBuilder()
    for i, button in enumerate(data['menu']):
        keyboard.add(InlineKeyboardButton(text=str(button), callback_data=str(i)))
    keyboard.add(InlineKeyboardButton(text='Другое', callback_data='other'))
    return keyboard.adjust(1).as_markup()


async def keyboard(enum, buttn):
    keyboard = InlineKeyboardBuilder()
    for i, button in enumerate(data['menu'][buttn]):
        keyboard.add(InlineKeyboardButton(text=str(button), callback_data=str(enum) + "_"+str(i)))
    keyboard.add(InlineKeyboardButton(text='Другое', callback_data='other'))
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