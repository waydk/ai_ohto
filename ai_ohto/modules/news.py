import requests
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup

from ai_ohto.bot import dp
from ai_ohto.utils.db_api import db_helpers

news_callback = CallbackData("act", "title")
main_news_callback = CallbackData("act", "title")

news_keyboard = InlineKeyboardMarkup()
yes_button = InlineKeyboardButton(text="yes", callback_data=news_callback.new("yes"))
no_button = InlineKeyboardButton(text="no", callback_data=news_callback.new("no"))
news_keyboard.insert(yes_button)
news_keyboard.insert(no_button)


async def change_news_status(message: types.Message):
    """
    To send news or not
    :param message:
    :return:
    """
    await message.answer("By clicking on the buttons below, you can decide whether or not to send you news",
                         reply_markup=news_keyboard)


async def yes_status(call: CallbackQuery):
    """
    Send news
    :param call:
    :return:
    """
    await call.answer("News will be sent", show_alert=True)
    await db_helpers.update_news_status(call.from_user.id, True)


async def no_status(call: CallbackQuery):
    """
    Not send news
    :param call:
    :return:
    """
    await call.answer("News will not be sent", show_alert=True)
    await db_helpers.update_news_status(call.from_user.id, False)


scheduler = AsyncIOScheduler()


async def send_anime_news(dp: Dispatcher):
    """
    Send news to users
    :param dp:
    :return:
    """
    users = await db_helpers.select_all_users()
    response_news = requests.get(url="https://www.animenewsnetwork.com/news/anime/")
    soup = BeautifulSoup(response_news.text, 'html.parser')
    items = soup.find_all("div", class_="herald box news")
    anime_news = []
    for item in items[:3]:
        anime_news.append(
            {
                "image": "https://www.animenewsnetwork.com" + item.find("div", class_="thumbnail lazyload").get(
                    "data-src"),
                "title": item.find("h3").get_text(),
                "link": "https://www.animenewsnetwork.com" + item.find("h3").find("a").get("href")
            }
        )
    for user in users:
        for anime in anime_news:
            await dp.bot.send_photo(chat_id=user.id, photo=anime['image'], caption=f"{anime['title']}\n"
                                                                                   f"<a href='"
                                                                                   f"{anime['link']}'"
                                                                                   f">Read more...</a>")


def schedule_anime_news():
    """
    When to send news
    :return:
    """
    scheduler.add_job(send_anime_news, "cron", day_of_week='mon-sun', hour=9, minute=3, args=(dp,))


scheduler.start()
schedule_anime_news()
