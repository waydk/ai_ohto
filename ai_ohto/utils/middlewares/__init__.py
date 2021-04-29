from .throttling import ThrottlingMiddleware
from ai_ohto.bot import dp

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
