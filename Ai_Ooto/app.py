from aiogram import executor

from Ai_Ooto.utils.notify_admins import on_startup_notify
from Ai_Ooto.utils import middlewares


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    from Ai_Ooto.modules import dp
    executor.start_polling(dp, on_startup=on_startup)
