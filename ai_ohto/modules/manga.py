import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

manga_query = """
query ($id: Int,$search: String) { 
      Media (id: $id, type: MANGA,search: $search) { 
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
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""

manga_url = 'https://graphql.anilist.co'


async def manga_info(message: types.Message):
    """
    Responds to the /manga <title> command
    :param message:
    :return:
    """
    manga = message.text
    find = ' '.join(manga.split(' ')[1:])

    logger.info(f"{message.from_user.full_name} send /manga {find}")

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

        await message.answer(f"{title} <code>({native_title})</code>\n"
                             f"Type: <b>{manga_data['type']}</b>\n"
                             f"Score: <b>{manga_data['averageScore']}</b>\n"
                             f"Genres: <code>{' '.join(manga_data['genres'])}</code>\n"
                             f"Status <b>{manga_data['status']}</b>\n\n"
                             f"Description: <i>{str(manga_data['description']).replace('<br>', ' ')}</i>"
                             f"<a href='{manga_data['bannerImage']}'>&#xad</a>", reply_markup=manga_keyboard)
    else:
        logger.info(f"manga not found --> status code: {status_code} \n")
        await message.answer("<code>Not found 😭 </code>")
