from aiogram import executor

from ai_ohto.utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    from ai_ohto.modules import dp
    executor.start_polling(dp, on_startup=on_startup)