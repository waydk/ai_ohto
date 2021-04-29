from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram_broadcaster import MessageBroadcaster

from ai_ohto.utils.db_api import db_helpers


async def broadcast_info(message: types.Message, state: FSMContext):
    """
    Responds to the /broadcast command and set state
    :param message:
    :param state:
    :return:
    """
    await message.answer("Enter the message to be sent in one message")
    await state.set_state("message")


async def broadcast(message: types.Message, state: FSMContext):
    """
    Mailing to users
    :param message:
    :param state:
    :return:
    """
    chats = []
    users = await db_helpers.select_all_users()
    for user in users:
        chats.append(user.id)
    await MessageBroadcaster(chats=chats, message=message).run()
    await state.finish()
