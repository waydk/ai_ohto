from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from Ai_Ooto.loader import dp


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer_photo("https://i.pinimg.com/originals/bc/0a/8c/bc0a8c599ed6bb909cadfc68d1298119.jpg",
                               caption="Hi, I'm Ai Ooto")
