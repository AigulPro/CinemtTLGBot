import datetime
import pytz
import prettytable as pt
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import config
from apiParser import get_weather, get_weather_for_next_days

bot = Bot(token=config.TOKEN_API_TELEGRAM)
dp = Dispatcher(bot=bot)
import html


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
kb_menu.add(KeyboardButton('📆 На 3 дня'))
kb_menu.insert(KeyboardButton('📆 На 5 дней'))
kb_menu.add(KeyboardButton('🛠 Настройки'))


# обработчик который обрабатывает команду start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer("  Привет!\n Сначала поделись геолокацией!🕹\n Или отправь мне название города! 🌆",
                         reply_markup=kb_start)


# Получаем геолокацию и сохраняем ее
@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    COORDINATES_DATA[message.from_user.id] = COORDINATES(message.location.longitude, message.location.latitude)
    await message.answer('Отлично!', reply_markup=kb_menu)


# Выводим погода на текущий день
@dp.message_handler(Text(equals="🌞 Сегодня"))
async def get_today_weather(message: types.Message):
    wthr = get_weather(COORDINATES_DATA[message.from_user.id])
    data_now = datetime.datetime.now(tz=pytz.timezone("Asia/Yekaterinburg")).strftime("%d.%m.%Y")
    await message.answer(f'{data_now}\n{wthr.location}, {wthr.description}\n'
                         f'Температура: {wthr.temperature}°C\n По ощущениям {wthr.temperature_feeling}°C')


# Выводим погода на завтра
@dp.message_handler(Text(equals="🌚 Завтра"))
async def get_today_weather(message: types.Message):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[message.from_user.id])
    date_weather = datetime.datetime.strptime(weather_data['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
    location = get_weather(COORDINATES_DATA[message.from_user.id]).location
    await message.answer(f'Завтра {date_weather}\n {location}, {weather_data["weather"][0]["description"]}\n'
                         f'Температура: {weather_data["main"]["temp"]}°C\n'
                         f' По ощущениям {weather_data["main"]["feels_like"]}°C')


def get_table(weather_data, weather_now):
    table = pt.PrettyTable(['Дата', '°C', 'Ощущается'])
    table.align['Дата'] = 'l'
    table.align['°C'] = 'r'
    table.align['Ощущается'] = 'с'

    data_now = datetime.datetime.now(tz=pytz.timezone("Asia/Yekaterinburg")).strftime("%d.%m")
    data = [(data_now, int(weather_now.temperature), int(weather_now.temperature_feeling))]

    for i in weather_data:
        data.append(
            (datetime.datetime.strptime(i['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime("%d.%m"), int(i['main']['temp']),
             int(i['main']['feels_like']))
        )

    for symbol, price, change in data:
        table.add_row([symbol, price, change])

    return table


# Выводим погоду на 3 дня
@dp.message_handler(Text(equals="📆 На 3 дня"))
async def get_today_weather(message: types.Message):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[message.from_user.id], 3)
    weather_now = get_weather(COORDINATES_DATA[message.from_user.id])
    table = get_table(weather_data, weather_now)
    await message.answer(f'<pre>{table}</pre>', parse_mode=types.ParseMode.HTML)


# Выводим погоду на 5 дней
@dp.message_handler(Text(equals='📆 На 5 дней'))
async def get_tomorrow_weather(message: types.Message):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[message.from_user.id], 5)
    weather_now = get_weather(COORDINATES_DATA[message.from_user.id])
    table = get_table(weather_data, weather_now)
    await message.answer(f'<pre>{table}</pre>', parse_mode=types.ParseMode.HTML)
