from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ai_ohto.loader import dp
from ai_ohto.utils.db_api import db_helpers

main_markup = InlineKeyboardMarkup(row_width=2)
anime_button = InlineKeyboardButton(text="anime", switch_inline_query_current_chat='anime ')
manga_button = InlineKeyboardButton(text="manga", switch_inline_query_current_chat='manga ')
character_button = InlineKeyboardButton(text="character", switch_inline_query_current_chat='char ')

main_markup.insert(anime_button)
main_markup.insert(manga_button)
main_markup.insert(character_button)


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer_photo("https://w.wallhaven.cc/full/57/wallhaven-577221.jpg",
                               caption="Hi, I'm Ai Ohto\n"
                                       "By clicking on the buttons below, you can try the inline mode\n"
                                       "Created by <a href='https://t.me/waydk'>waydk</a>", reply_markup=main_markup)
    await db_helpers.add_user(id_user=message.from_user.id,
                              name=message.from_user.full_name)