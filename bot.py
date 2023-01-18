import time, datetime, pytz
import logging
from dataclasses import dataclass

from aiogram.dispatcher.filters import Text

import config
import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apiParser import get_weather

bot = Bot(token=config.TOKEN_API_TELEGRAM)
dp = Dispatcher(bot=bot)


# Для хранения координат пользователя
class COORDINATES:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat


COORDINATES_DATA = {}

# Клавиатура
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add(KeyboardButton('🕹 Поделиться Геолокацией', request_location=True))

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(KeyboardButton('🌞 Сегодня'))
kb_menu.insert(KeyboardButton('🌚 Завтра'))
kb_menu.add(KeyboardButton('📆 На 5 дней'))
kb_menu.insert(KeyboardButton('📆 На 7 дней'))
kb_menu.insert(KeyboardButton('📆 На 10 дней'))
kb_menu.add(KeyboardButton('🛠 Настройки'))


# обработчик который обрабатывает команду start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    print('I say hello!')
    await message.answer("  Привет!\n Сначала поделись геолокацией!🕹\n Или отправь мне название города! 🌆",
                         reply_markup=kb_start)


# Получаем геолокацию и сохраняем ее
@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    COORDINATES_DATA[message.from_user.id] = COORDINATES(message.location.longitude
                                                         , message.location.latitude)
    print(COORDINATES_DATA)
    await message.answer('Отлично!', reply_markup=kb_menu)


# Выводим погода на текущий день
@dp.message_handler(Text(equals="🌞 Сегодня"))
async def get_today_weather(message: types.Message):
    wthr = get_weather(COORDINATES_DATA[message.from_user.id])
    data_now = datetime.datetime.now(tz=pytz.timezone("Asia/Yekaterinburg")).strftime("%Y-%m-%d")
    await message.answer(f'{data_now}\n{wthr.location}, {wthr.description}\n' \
                         f'Температура: {wthr.temperature}°C\n По ощущениям {wthr.temperature_feeling}°C')


# Выводим погоду на 5 дней
@dp.message_handler(Text(equals='📆 На 5 дней'))
async def get_tomorrow_weather(message: types.Message):
    coord = COORDINATES_DATA[message.from_user.id]
    url = config.FIVE_DAYS_WEATHER_API_CALL.format(latitude=coord.lat, longitude=coord.lon)
    result = requests.get(url)
    print(result.json())
    await message.answer('Успех!', reply_markup=kb_menu)
