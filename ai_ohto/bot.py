from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from environs import Env

# Read env file
env = Env()
env.read_env()

token = env.str("BOT_TOKEN")

# Bot, storage and dispatcher instances
bot = Bot(token=token, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
