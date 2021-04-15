from aiogram import executor

from ai_ohto.utils.db_api import db_gino
from ai_ohto.utils.db_api.db_gino import db
from ai_ohto.utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)
    await db_gino.on_startup(dp)
    await db.gino.create_all()


if __name__ == '__main__':
    from ai_ohto.modules import dp
    executor.start_polling(dp, on_startup=on_startup)
