import time
import logging
from dataclasses import dataclass

from aiogram.dispatcher.filters import Text

import config
import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apiParser import get_weather

COORDINATES = {
    'lon': 0,
    'lat': 0,
}

bot = Bot(token=config.TOKEN_API_TELEGRAM)
dp = Dispatcher(bot=bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('🕹 Поделиться Геолокацией', request_location=True))

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(KeyboardButton('🌞 Сегодня'))


# обработчик который обрабатывает команду start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    print('I say hello!')
    await message.answer("  Привет!\n Сначала поделись геолокацией!🕹\n Или отправь мне название города! 🌆",
                         reply_markup=kb)


# Получаем геолокацию и выводим ее
@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    COORDINATES['lat'] = message.location.latitude
    COORDINATES['lon'] = message.location.longitude
    await message.answer('Отлично!', reply_markup=kb_menu)


@dp.message_handler(Text(equals="🌞 Сегодня"))
async def get_today_weather(message: types.Message):
    wthr = get_weather(COORDINATES)
    await message.reply(f'{wthr.location}, {wthr.description}\n' \
                        f'Temperature is {wthr.temperature}°C, feels like {wthr.temperature_feeling}°C')
