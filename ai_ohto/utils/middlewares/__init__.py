from .throttling import ThrottlingMiddleware
from ai_ohto.loader import dp

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
