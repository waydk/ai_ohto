from asyncpg import UniqueViolationError

from ai_ohto.utils.db_api.schemas.user import User


async def add_user(id_user: int, name: str):
    try:
        user = User(id=id_user, name=name)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users
