import time
import logging
import config
import requests
from aiogram import Bot, Dispatcher, types,executor

bot = Bot(token=config.TOKEN_API_TELEGRAM)
dp = Dispatcher(bot=bot)


#обработчик который обрабатывает команду start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat=40,7143&lon=-74,006&appid={config.TOKEN_API_WEATHER}&units=metric")

    await message.reply(result.text)

