import datetime
import pytz
import config
import prettytable as pt
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from apiParser import get_weather, get_weather_for_next_days
from keybords import *

bot = Bot(token=config.TOKEN_API_TELEGRAM)
dp = Dispatcher(bot=bot)
import html


# Для хранения координат пользователя
class COORDINATES:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat


COORDINATES_DATA = {}


# Формируем таблицу погоды для диапазона дат
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


# Формируем таблицу дополнительной информации о погоде для диапазона дат
def get_table_dop_info(weather_data, weather_now):
    table = pt.PrettyTable(['Мин°C', 'Макс°C', 'Ветер㎧'])
    table.align['Мин °C'] = 'l'
    table.align['Макс °C'] = 'r'
    table.align['Ветер ㎧'] = 'с'

    data = [(int(weather_now.min_temperature), int(weather_now.max_temperature), weather_now.wind_speed)]

    for i in weather_data:
        data.append(
            (int(i['main']['temp_min']), int(i['main']['temp_max']), i['wind']["speed"]),
        )

    for symbol, price, change in data:
        table.add_row([symbol, price, change])

    return table


# Получаем направление ветра на русском ящыке
def get_translate_direction(eng_word):
    translater = {
        'North': 'Север',
        'West': 'Запад',
        'East': 'Восток',
        'South': 'Юг',
    }
    return translater[eng_word]


# обработчик который обрабатывает команду start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer("Привет!\nПоделись со мной геолокацией!🕹\n",
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
                         f'Температура: {int(wthr.temperature)}°C\nПо ощущениям {int(wthr.temperature_feeling)}°C',
                         reply_markup=inline_kb)


# Выводим погода на завтра
@dp.message_handler(Text(equals="🌚 Завтра"))
async def get_today_weather(message: types.Message):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[message.from_user.id])
    date_weather = datetime.datetime.strptime(weather_data['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
    location = get_weather(COORDINATES_DATA[message.from_user.id]).location
    await message.answer(f'Завтра {date_weather}\n{location}, {weather_data["weather"][0]["description"]}\n'
                         f'Температура: {int(weather_data["main"]["temp"])}°C\n'
                         f'По ощущениям {int(weather_data["main"]["feels_like"])}°C', reply_markup=inline_kb_tommorow)


# Выводим погоду на 3 дня
@dp.message_handler(Text(equals="📆 На 3 дня"))
async def get_today_weather(message: types.Message):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[message.from_user.id], 3)
    weather_now = get_weather(COORDINATES_DATA[message.from_user.id])
    table = get_table(weather_data, weather_now)
    await message.answer(f'<pre>{table}</pre>', parse_mode=types.ParseMode.HTML, reply_markup=inline_kb_many_days)


# Выводим погоду на 5 дней
@dp.message_handler(Text(equals='📆 На 5 дней'))
async def get_tomorrow_weather(message: types.Message):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[message.from_user.id], 5)
    weather_now = get_weather(COORDINATES_DATA[message.from_user.id])
    table = get_table(weather_data, weather_now)
    await message.answer(f'<pre>{table}</pre>', parse_mode=types.ParseMode.HTML, reply_markup=inline_kb_many_5days)

@dp.callback_query_handler(text='sunrise')
async def process_callback_button1(callback_query: types.CallbackQuery):
    weather_now = get_weather(COORDINATES_DATA[callback_query.from_user.id])
    await callback_query.message.answer(
        f'Восход :{weather_now.sunrise.strftime("%H:%M:%S")}\nЗакат :{weather_now.sunset.strftime("%H:%M:%S")}')
    await callback_query.answer()



# Работа с дополнительной информацией---------------------------------------------------------------------------------

# Вывол солнца для "сегодня"
@dp.callback_query_handler(text='sunrise')
async def process_callback_button1(callback_query: types.CallbackQuery):
    weather_now = get_weather(COORDINATES_DATA[callback_query.from_user.id])
    await callback_query.message.answer(
        f'Восход :{weather_now.sunrise.strftime("%H:%M:%S")}\nЗакат :{weather_now.sunset.strftime("%H:%M:%S")}')
    await callback_query.answer()


# вывод ветра для "сегодня"
@dp.callback_query_handler(text='wind')
async def process_callback_today(callback_query: types.CallbackQuery):
    weather_now = get_weather(COORDINATES_DATA[callback_query.from_user.id])
    await callback_query.message.answer(
        f'Направление :{get_translate_direction(weather_now.wind_direction)}\nСкорость ветра :{weather_now.wind_speed}м/с')
    await callback_query.answer()


# Вывол подробнее для "завтра"
@dp.callback_query_handler(text='dop_info')
async def process_callback_tommorow(callback_query: types.CallbackQuery):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[callback_query.from_user.id])
    date_weather = datetime.datetime.strptime(weather_data['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
    await callback_query.message.answer(
        f'Мин.темп:{int(weather_data["main"]["temp_min"])}°C\n'
        f'Макс.темп:{int(weather_data["main"]["temp_min"])}°C\n'
        f'Скорость ветра:{weather_data["wind"]["speed"]}м/с')
    await callback_query.answer()


# Вывод подробнее для "3 дней"
@dp.callback_query_handler(text='dop_info_table')
async def get_tomorrow_weather(callback_query: types.CallbackQuery):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[callback_query.from_user.id], 3)
    weather_now = get_weather(COORDINATES_DATA[callback_query.from_user.id])
    table = get_table_dop_info(weather_data, weather_now)
    await callback_query.message.answer(f'<pre>{table}</pre>', parse_mode=types.ParseMode.HTML)
    await callback_query.answer()


# Вывод подробнее для "5 дней"
@dp.callback_query_handler(text='dop_info_5table')
async def get_tomorrow_weather(callback_query: types.CallbackQuery):
    weather_data = get_weather_for_next_days(COORDINATES_DATA[callback_query.from_user.id], 5)
    weather_now = get_weather(COORDINATES_DATA[callback_query.from_user.id])
    table = get_table_dop_info(weather_data, weather_now)
    await callback_query.message.answer(f'<pre>{table}</pre>', parse_mode=types.ParseMode.HTML)
    await callback_query.answer()
