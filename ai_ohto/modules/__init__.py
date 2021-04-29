from aiogram import Dispatcher, types
from environs import Env

from .anime import anime_info
from .broadcaster import broadcast_info, broadcast
from .character import character_info
from .errors import errors_handler
from .help import show_help
from .inline import inline_query
from .manga import manga_info
from .news import change_news_status, yes_status, news_callback, no_status, main_news_callback
from .start import start, change_anime_news_status

env = Env()
env.read_env()

admins = env.str("ADMINS")


def setup(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
    dp.register_message_handler(anime_info, commands="anime")
    dp.register_message_handler(broadcast_info, commands="broadcast", user_id=admins)
    dp.register_message_handler(broadcast, state="message", content_types=types.ContentTypes.ANY)
    dp.register_message_handler(character_info, commands="char")
    dp.register_message_handler(show_help, commands="help")
    dp.register_inline_handler(inline_query)
    dp.register_message_handler(manga_info, commands="manga")
    dp.register_message_handler(change_news_status, commands="news")
    dp.register_callback_query_handler(yes_status, news_callback.filter(title="yes"))
    dp.register_callback_query_handler(no_status, news_callback.filter(title="no"))
    dp.register_message_handler(start, commands="start")
    dp.register_callback_query_handler(change_anime_news_status, main_news_callback.filter(title="anime_news"))
