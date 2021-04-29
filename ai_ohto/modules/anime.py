import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
anime_url = "https://graphql.anilist.co"


async def anime_info(message: types.Message):
    """
    Responds to the /anime <title> command
    :param message:
    :return:
    """
    anime = message.text
    find = ' '.join(anime.split(' ')[1:])
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

        await message.answer(f"{title} <code>({native_title})</code>\n"
                             f"Type: <b>{anime_data['type']}</b>\n"
                             f"Score: <b>{anime_data['averageScore']}</b>\n"
                             f"Duration: <b>{anime_data['duration']}</b>\n"
                             f"Format: <b>{anime_data['format']}</b>\n"
                             f"Genres: <code>{' '.join(anime_data['genres'])}</code>\n"
                             f"Status <b>{anime_data['status']}</b>\n\n"
                             f"Description: <i>{str(anime_data['description']).replace('<br>', ' ')}</i>"
                             f"<a href='{image}'>&#xad</a>", reply_markup=anime_keyboard)
    else:
        await message.answer("<code>Not found 😭 </code>")
