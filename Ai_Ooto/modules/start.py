from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Ai_Ooto.loader import dp

main_markup = InlineKeyboardMarkup()
anime_button = InlineKeyboardButton(text="anime", switch_inline_query_current_chat='anime ')
manga_button = InlineKeyboardButton(text="manga", switch_inline_query_current_chat='manga ')
main_markup.insert(anime_button)
main_markup.insert(manga_button)


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer_photo("https://w.wallhaven.cc/full/57/wallhaven-577221.jpg",
                               caption="Hi, I'm Ai Ooto", reply_markup=main_markup)
