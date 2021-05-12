from aiogram import Dispatcher, executor
from loguru import logger

from ai_ohto import modules
from ai_ohto.bot import dp
from ai_ohto.utils.db_api.db_gino import db, POSTGRES_URI


async def startup(dispatcher: Dispatcher):
    """Triggers on startup."""

    # Setup handlers
    logger.info("Configuring modules...")
    modules.setup(dispatcher)

    # Working with the database
    logger.info("The database is working...")
    await db.set_bind(POSTGRES_URI)
    await db.gino.create_all()

    # Set command hints
    logger.info("Start polling")


if __name__ == "__main__":
    # Start long-polling mode
    executor.start_polling(dp, on_startup=startup, skip_updates=True)
