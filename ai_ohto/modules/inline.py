import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ai_ohto.loader import dp
from ai_ohto.modules.anime import anime_query, anime_url
from ai_ohto.modules.character import character_url, character_query, shorten
from ai_ohto.modules.manga import manga_url, manga_query
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

    elif inline_input.split()[0] == 'manga':
        if len(inline_input.split()) == 1:
            await query.answer(
                results=results,
                switch_pm_text='Search an manga',
                switch_pm_parameter='start'
            )
            return
        find = ' '.join(inline_input.split()[1:])
        variables = {"search": find}
        status_code = requests.post(manga_url, json={'query': manga_query,
                                                     'variables': variables}).status_code
        if status_code == 200:
            manga_data = requests.post(manga_url, json={'query': manga_query,
                                                        'variables': variables}).json()['data'].get('Media', None)
            manga_keyboard = InlineKeyboardMarkup()
            more_button = InlineKeyboardButton(text="🟡 More ", url=manga_data['siteUrl'])
            manga_keyboard.insert(more_button)
            if manga_data['title']['english']:
                title = manga_data['title']['english']
            else:
                title = manga_data['title']['romaji']
            if manga_data['title']['native']:
                native_title = manga_data['title']['native']
            else:
                native_title = 'not found ;)'

            results.append(
                types.InlineQueryResultArticle(
                    id=manga_data['id'],
                    title=title,
                    description=manga_data['description'],
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"{title} <code>({native_title})</code>\n"
                                     f"Type: <b>{manga_data['type']}</b>\n"
                                     f"Score: <b>{manga_data['averageScore']}</b>\n"
                                     f"Genres: <code>{' '.join(manga_data['genres'])}</code>\n"
                                     f"Status <b>{manga_data['status']}</b>\n\n"
                                     f"Description: <i>{str(manga_data['description']).replace('<br>', ' ')}</i>"
                                     f"<a href='{manga_data['bannerImage']}'>&#xad</a>"),
                    reply_markup=manga_keyboard,
                    thumb_url=manga_data['bannerImage']
                )
            )
            await query.answer(results=results, cache_time=0)

    elif inline_input.split()[0] == 'char':
        if len(inline_input.split()) == 1:
            await query.answer(
                results=results,
                switch_pm_text='Search an character',
                switch_pm_parameter='start'
            )
            return
        find = ' '.join(inline_input.split(' ')[1:])
        variables = {"query": find}
        status_code = requests.post(character_url, json={'query': character_query,
                                                         'variables': variables}).status_code
        if status_code == 200:
            character_data = requests.post(character_url, json={'query': character_query,
                                                                'variables': variables}).json()['data'].get(
                'Character',
                None)
            char_keyboard = InlineKeyboardMarkup()
            more_button = InlineKeyboardButton(text="🟡 More ", url=character_data['siteUrl'])
            char_keyboard.insert(more_button)
            description = shorten(str(character_data['description']).replace("__", ''), character_data['siteUrl'])
            results.append(
                types.InlineQueryResultPhoto(
                    photo_url=character_data['image']['large'],
                    id=character_data['id'],
                    title=character_data['name']['full'],
                    description=str(character_data['description']).replace("__", ''),

                    caption=f"<code>{character_data['name']['full']}</code>\n"
                            f"<b>Favourites</b>: <b>{character_data['favourites']}</b>\n"
                            f"{description}\n",
                    reply_markup=char_keyboard,
                    thumb_url=character_data['image']['large']))
            await query.answer(results=results, cache_time=0)
