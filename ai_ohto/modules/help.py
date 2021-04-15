from aiogram import types
from aiogram.dispatcher.filters import Command

from ai_ohto.loader import dp
from ai_ohto.modules.start import main_markup


@dp.message_handler(Command("help"))
async def show_help(message: types.Message):
    await message.answer_photo(photo='https://w.wallhaven.cc/full/o3/wallhaven-o33j29.jpg',
                               caption="Available commands: \n\n"
                                       "/anime <code>anime title</code> - find anime\n"
                                       "/manga <code> manga title</code> - find manga\n"
                                       "/char <code> manga title</code> - find character\n\n"
                                       "<b>By clicking on the buttons below, you can try the inline mode</b>",
                               reply_markup=main_markup)
