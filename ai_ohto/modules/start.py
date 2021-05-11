from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from ai_ohto.modules.news import main_news_callback, news_keyboard
from ai_ohto.utils.db_api import db_helpers

main_markup = InlineKeyboardMarkup(row_width=2)
anime_button = InlineKeyboardButton(text="anime", switch_inline_query_current_chat='anime ')
manga_button = InlineKeyboardButton(text="manga", switch_inline_query_current_chat='manga ')
character_button = InlineKeyboardButton(text="character", switch_inline_query_current_chat='char ')
open_source_button = InlineKeyboardButton(text="open source", url='https://github.com/waydk/AiOhto')
news_button = InlineKeyboardButton(text="news", callback_data=main_news_callback.new("anime_news"))

main_markup.insert(anime_button)
main_markup.insert(manga_button)
main_markup.insert(character_button)
main_markup.insert(open_source_button)
main_markup.insert(news_button)


async def start(message: types.Message):
    """
    Responds to the /start command
    :param message:
    :return:
    """
    await message.answer_photo("https://s4.anilist.co/file/anilistcdn/character/large/b199892-IUa7rBAT4j9H.png",
                               caption="• Hi, I'm Ai Ohto • \n\n"
                                       "By clicking on the buttons below, you can try the inline mode\n\n"
                                       "Created by <a href='https://t.me/waydk'>waydk</a>\n\n"
                                       "• Need help? /help •", reply_markup=main_markup)
    await db_helpers.add_user(id_user=message.from_user.id,
                              name=message.from_user.full_name, status_news=True)


async def change_anime_news_status(call: CallbackQuery):
    """
    Change news status
    :param call:
    :return:
    """
    await call.answer(cache_time=5)
    await call.message.answer("By clicking on the buttons below, you can decide whether or not to send you news",
                              reply_markup=news_keyboard)
