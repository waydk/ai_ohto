from aiogram import types
from loguru import logger

from ai_ohto.modules.start import main_markup


async def show_help(message: types.Message):
    """
    Responds to the /help command
    :param message:
    :return:
    """
    logger.info(f"{message.from_user.full_name} send /help")
    await message.answer_photo(photo='https://w.wallhaven.cc/full/o3/wallhaven-o33j29.jpg',
                               caption="Available commands: \n\n"
                                       "/anime <code>anime title</code> - find anime\n"
                                       "/manga <code> manga title</code> - find manga\n"
                                       "/char <code> manga title</code> - find character\n"
                                       "/news - change anime news status\n\n"
                                       "<b>By clicking on the buttons below, you can try the inline mode</b>",
                               reply_markup=main_markup)
