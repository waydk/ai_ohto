from asyncpg import UniqueViolationError

from ai_ohto.utils.db_api.schemas.user import User


async def add_user(id_user: int, name: str, status_news: bool):
    try:
        user = User(id=id_user, name=name, status_news=status_news)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.where(User.status_news == True).gino.all()
    return users


async def update_news_status(id_user, status):
    user = await User.query.where(User.id == id_user).gino.first()
    await user.update(status_news=status).apply()