from .throttling import ThrottlingMiddleware
from ...loader import dp

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
