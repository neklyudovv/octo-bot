from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.handlers import CallbackQueryHandler

from random import randint

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from engine.parser import data
import engine.keyboards as kb

from engine.docs import main as main_docs

from engine.attachments import main as main_att


router = Router()


class Form(StatesGroup):
    text = State()


# "Другое"
@router.callback_query(F.data == 'other')
async def other_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.text)
    await callback.message.edit_text(data['other_message'], reply_markup=kb.back_kb.as_markup())


@router.message(F.photo)
async def handle_attachments(message: Message, state: FSMContext):
    current_state = await state.get_state()

    rr = str(randint(1, 9999999))
    file_name = 'downloads/' + rr + '.jpg'
    await message.bot.download(file=message.photo[-1].file_id, destination=file_name)
    file_id = main_att(rr + '.jpg', file_name)
    main_docs('https://drive.google.com/file/d/' + file_id + '/view')

    if current_state is not None:
        await state.update_data(text=message.caption)
        other_data = await state.get_data()
        await state.clear()
        await send_other(message, other_data=other_data)


@router.message(F.text, Form.text)
async def process_other(message: Message, state: FSMContext):
    if message.text is None:
        await state.set_state(Form.text)
    else:
        await state.update_data(text=message.text)
        other_data = await state.get_data()
        await state.clear()
        await send_other(message, other_data=other_data)


@router.callback_query(F.data == 'other_back')
async def cancel_other(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await callback.message.edit_text(data["greeting_message2"], reply_markup=await kb.menu())
        return
    await state.clear()
    await callback.message.edit_text(data["greeting_message2"], reply_markup=await kb.menu())


async def send_other(message: Message, other_data):
    text = other_data['text']
    main_docs(text)
    await message.answer('Мы получили твое обращение, спасибо!', reply_markup=kb.back_kb.as_markup())


@router.message(CommandStart())  # /start
async def command_start_handler(message: Message):
    await message.answer(data["greeting_message"], reply_markup=kb.greet_kb.as_markup())  # await menu())


@router.callback_query(F.data == 'start')  # inline Начало
async def start(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(data["greeting_message2"], reply_markup=await kb.menu())


@router.callback_query()
class MyHandler(CallbackQueryHandler):
    async def handle(self):
        user_choice = self.data['event_update'].callback_query.data
        if user_choice == 'home':  # inline на главную
            await self.message.edit_text(data["greeting_message2"], reply_markup=await kb.menu())

        if user_choice.count("_") == 0:
            for i, button in enumerate(data['menu']):  # inline category
                if user_choice == str(i):
                    await self.message.edit_text(str(button).upper(), reply_markup=await kb.keyboard(i, button))
        else:
            for i, button in enumerate(data['menu']):
                for j, buttn in enumerate(data['menu'][button]):
                    if user_choice == str(i) + "_" + str(j):
                        await self.message.edit_text(str(data['menu'][button][buttn]),
                                                     reply_markup=kb.other_kb.as_markup())
