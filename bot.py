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
    result = requests.get(f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=44.34&lon=10.99&appid={config.TOKEN_API_WEATHER}")

    await message.reply(result.text)

