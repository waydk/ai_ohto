import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ai_ohto.loader import dp
from ai_ohto.modules.start import main_markup


@dp.inline_handler()
async def inline_query(query: types.InlineQuery):
    results = []
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

    elif inline_input.split()[0] == 'anime':
        anime_query = """
           query ($id: Int,$search: String) {
              Media (id: $id, type: ANIME,search: $search) {
                id
                title {
                  romaji
                  english
                  native
                }
                description (asHtml: false)
                startDate{
                    year
                  }
                  episodes
                  season
                  type
                  format
                  status
                  duration
                  siteUrl
                  studios{
                      nodes{
                           name
                      }
                  }
                  trailer{
                       id
                       site
                       thumbnail
                  }
                  averageScore
                  genres
                  bannerImage
              }
            }
        """
        url = "https://graphql.anilist.co"

        if len(inline_input.split()) == 1:
            await query.answer(
                results=results,
                switch_pm_text='Search an anime',
                switch_pm_parameter='start'
            )
            return
        find = ' '.join(inline_input.split()[1:])
        variables = {"search": find}
        status_code = requests.post(url, json={'query': anime_query,
                                              'variables': variables}).status_code
        if status_code == 200:
            anime_data = requests.post(url, json={'query': anime_query,
                                                  'variables': variables}).json()['data'].get('Media', None)
            anime_url = anime_data.get('siteUrl')
            image = anime_url.replace('anilist.co/anime/', 'img.anili.st/media/')
            anime_keyboard = InlineKeyboardMarkup()
            more_button = InlineKeyboardButton(text="🟡 More ", url=anime_url)
            anime_keyboard.insert(more_button)
            if anime_data['title']['english']:
                title = anime_data['title']['english']
            else:
                title = anime_data['title']['romaji']
            results.append(
                types.InlineQueryResultArticle(
                    id=anime_data['id'],
                    title=title,
                    description=anime_data['description'],
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"🔵 {title}\n"
                                     f"Type: {anime_data['type']}\n"
                                     f"Score: {anime_data['averageScore']}\n"
                                     f"Duration: {anime_data['duration']}\n"
                                     f"Format: {anime_data['format']}\n"
                                     f"Description: <i>{str(anime_data['description']).replace('<br>', ' ')}</i>"
                                     f"<a href='{image}'>&#xad</a>"),
                    reply_markup=anime_keyboard,
                    thumb_url=image
                )
            )
            await query.answer(results=results, cache_time=0)
