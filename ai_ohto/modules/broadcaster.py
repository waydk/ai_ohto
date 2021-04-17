from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram_broadcaster import MessageBroadcaster

from ai_ohto.loader import dp
from ai_ohto.utils.config import ADMINS
from ai_ohto.utils.db_api import db_helpers


@dp.message_handler(Command("broadcast"), user_id=ADMINS)
async def broadcast_info(message: types.Message, state: FSMContext):
    await message.answer("Enter the message to be sent in one message")
    await state.set_state("message")


@dp.message_handler(state="message")
async def broadcast(message: types.Message, state: FSMContext):
    chats = []
    users = await db_helpers.select_all_users()
    for user in users:
        chats.append(user.id)
    await MessageBroadcaster(chats=chats, message=message).run()
    await state.finish()
