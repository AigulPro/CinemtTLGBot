import time
import logging
import config
import requests
from aiogram import Bot, Dispatcher, types,executor
from coordinates import get_coordinates
from apiParser import get_weather

bot = Bot(token=config.TOKEN_API_TELEGRAM)
dp = Dispatcher(bot=bot)


#обработчик который обрабатывает команду start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):

    await message.reply('Привет')


@dp.message_handler(commands=['weather'])
async def start_bot(message: types.Message):

    wthr = get_weather(get_coordinates())
    print(wthr)
    await message.reply(f'{wthr.location}, {wthr.description}\n' \
           f'Temperature is {wthr.temperature}°C, feels like {wthr.temperature_feeling}°C')


# @dp.message_handler(commands=['weather'])
# async def weather(message: types.Message):
#     wthr = get_weather(get_coordinates())
#     await message.reply(wthr.location)