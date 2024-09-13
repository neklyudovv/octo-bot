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


async def handle_attachments(message: Message, state: FSMContext, attachment_type: str):
    current_state = await state.get_state()
    if attachment_type == 'video':
        video = message.video.file_name
        video_name = str(randint(1, 9999999))
        file_name = 'downloads/' + video_name + video[video.find('.')::]
        await message.bot.download(file=message.video.file_id, destination=file_name)
        file_id = main_att(video_name + video[video.find('.')::], file_name, message.video.mime_type)
    else:
        image_name = str(randint(1, 9999999))
        file_name = 'downloads/' + image_name + '.jpg'
        await message.bot.download(file=message.photo[-1].file_id, destination=file_name)
        file_id = main_att(image_name + '.jpg', file_name, 'image/jpeg')

    main_docs('https://drive.google.com/file/d/' + file_id + '/view')
    if current_state and message.caption:
        await state.update_data(text=message.caption)
        other_data = await state.get_data()
        await state.clear()
        await send_other(message, other_data=other_data)


@router.message(F.video)
async def handle_video(message: Message, state: FSMContext):
    await handle_attachments(message, state, 'video')


@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    await handle_attachments(message, state, 'photo')


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
            for i, topic_button in enumerate(data['menu']):  # inline category
                if user_choice == str(i):
                    await self.message.edit_text(str(topic_button).upper(),
                                                 reply_markup=await kb.keyboard(i, topic_button))
        else:
            for i, topic_button in enumerate(data['menu']):
                for j, question_button in enumerate(data['menu'][topic_button]):  # inline кнопка в категории
                    if user_choice == str(i) + "_" + str(j):
                        await self.message.edit_text(str(data['menu'][topic_button][question_button]),
                                                     reply_markup=kb.other_kb.as_markup())
