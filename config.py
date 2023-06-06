from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = ''


bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)



