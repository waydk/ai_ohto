import requests
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup

from ai_ohto.loader import dp
from ai_ohto.utils.db_api import db_helpers

scheduler = AsyncIOScheduler()


async def send_anime_news(dp: Dispatcher):
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
    scheduler.add_job(send_anime_news, "cron", day_of_week='mon-sun', hour=15, minute=30, args=(dp,))


scheduler.start()
schedule_anime_news()
