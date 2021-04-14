import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ai_ohto.loader import dp
from ai_ohto.modules.anime import anime_query, anime_url
from ai_ohto.modules.start import main_markup


@dp.inline_handler()
async def inline_query(query: types.InlineQuery):
    results = []
    ai_photo = 'https://i.postimg.cc/J0px5LFm/1.png'
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

    elif inline_input.split()[0] == 'anime':
        if len(inline_input.split()) == 1:
            await query.answer(
                results=results,
                switch_pm_text='Search an anime',
                switch_pm_parameter='start'
            )
            return
        find = ' '.join(inline_input.split()[1:])
        variables = {"search": find}
        status_code = requests.post(anime_url, json={'query': anime_query,
                                                     'variables': variables}).status_code
        if status_code == 200:
            anime_data = requests.post(anime_url, json={'query': anime_query,
                                                        'variables': variables}).json()['data'].get('Media', None)
            anime_site = anime_data.get('siteUrl')
            image = anime_site.replace('anilist.co/anime/', 'img.anili.st/media/')
            anime_keyboard = InlineKeyboardMarkup()
            more_button = InlineKeyboardButton(text="🟡 More ", url=anime_site)
            anime_keyboard.insert(more_button)
            if anime_data['title']['english']:
                title = anime_data['title']['english']
            else:
                title = anime_data['title']['romaji']
            if anime_data['title']['native']:
                native_title = anime_data['title']['native']
            else:
                native_title = 'not found ;)'

            results.append(
                types.InlineQueryResultArticle(
                    id=anime_data['id'],
                    title=title,
                    description=anime_data['description'],
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"{title} <code>({native_title})</code>\n"
                                     f"Type: <b>{anime_data['type']}</b>\n"
                                     f"Score: <b>{anime_data['averageScore']}</b>\n"
                                     f"Duration: <b>{anime_data['duration']}</b>\n"
                                     f"Format: <b>{anime_data['format']}</b>\n"
                                     f"Genres: <code>{' '.join(anime_data['genres'])}</code>\n"
                                     f"Status <b>{anime_data['status']}</b>\n\n"
                                     f"Description: <i>{str(anime_data['description']).replace('<br>', ' ')}</i>"
                                     f"<a href='{image}'>&#xad</a>"),
                    reply_markup=anime_keyboard,
                    thumb_url=image
                )
            )
            await query.answer(results=results, cache_time=0)
