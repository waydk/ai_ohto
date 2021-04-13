from aiogram import types

from ai_ohto.loader import dp
from ai_ohto.modules.start import main_markup


@dp.inline_handler()
async def inline_query(query: types.InlineQuery):
    ai_photo = 'https://w.wallhaven.cc/full/o3/wallhaven-o33j29.jpg'
    inline_input = query.query.lower()
    if inline_input == '':
        await query.answer(
            results=[
                types.InlineQueryResultPhoto(
                    id=query.id,
                    thumb_url=ai_photo,
                    caption="Try me inline by clicking below",
                    photo_url=ai_photo,
                    reply_markup=main_markup,
                ),
            ],
            switch_pm_text="Click here to start again",
            switch_pm_parameter="start",
            cache_time=300
        )
