from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.handlers import CallbackQueryHandler

from engine.parser import data
import engine.keyboards as kb

router = Router()

@router.message(CommandStart()) #/start
async def command_start_handler(message: Message):
    await message.answer(data["greeting_message"], reply_markup=kb.greet_kb.as_markup())#await menu())


@router.callback_query(F.data == 'start') # inline Начало
async def start(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(data["greeting_message2"], reply_markup= await kb.menu())


@router.callback_query()
class MyHandler(CallbackQueryHandler):
    async def handle(self):
        user_choice = self.data['event_update'].callback_query.data
        if user_choice == 'home': # inline на главную
            await self.message.edit_text(data["greeting_message2"], reply_markup=await kb.menu())

        if user_choice == 'other':
            await self.message.edit_text(data['other_message'], reply_markup=kb.back_kb.as_markup())

        if user_choice.count("_") == 0:
            for i, button in enumerate(data['menu']): #inline category
                if user_choice == str(i):
                    await self.message.edit_text(str(button).upper(), reply_markup=await kb.keyboard(i, button))
        else:
            for i, button in enumerate(data['menu']):
                for j, buttn in enumerate(data['menu'][button]):
                    if user_choice == str(i) + "_" + str(j):
                        await self.message.edit_text(str(data['menu'][button][buttn]), reply_markup=kb.other_kb.as_markup())
       # else:
        #    for i, button in enumerate(data['menu']):



        #for i in data['menu']: # inline категория
        #    if user_choice == str(i):
        #        await self.message.edit_text(str(i).upper(), reply_markup=await kb.keyboard(i))
        #    for j in data['menu'][i]: # inline тема в категории
        #        if user_choice == str(j):
        #            await self.message.edit_text(str(data['menu'][i][j]), reply_markup=kb.other_kb.as_markup())