import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               favourites
               image {
                        large
               }
               description
        }
    }
"""

character_url = 'https://graphql.anilist.co'


def shorten(description, info="anilist.co"):
    """
    Shortens the description
    :param description:
    :param info:
    :return:
    """
    character_description = ""
    if len(description) > 700:
        description = description[0:500] + "...."
        character_description += f"<b>Description</b>: <i>{description}<a href='{info}'>Read more</a></i>"
    else:
        character_description += f"<b>Description</b>:<i>{description}</i>"
    return character_description


async def character_info(message: types.Message):
    """
    Responds to the /char <name> command
    :param message:
    :return:
    """
    character = message.text
    find = ' '.join(character.split(' ')[1:])
    variables = {"query": find}
    status_code = requests.post(character_url, json={'query': character_query,
                                                     'variables': variables}).status_code
    if status_code == 200:
        character_data = requests.post(character_url, json={'query': character_query,
                                                            'variables': variables}).json()['data'].get('Character',
                                                                                                        None)
        char_keyboard = InlineKeyboardMarkup()
        more_button = InlineKeyboardButton(text="🟡 More ", url=character_data['siteUrl'])
        char_keyboard.insert(more_button)
        description = shorten(str(character_data['description']).replace("__", ''), character_data['siteUrl'])
        await message.answer_photo(photo=character_data['image']['large'],
                                   caption=f"<code>{character_data['name']['full']}</code>\n"
                                           f"<b>Favourites</b>: <b>{character_data['favourites']}</b>\n"
                                           f"{description}\n",
                                   reply_markup=character_data)
    else:
        await message.answer("<code>Not found 😭 </code>")
