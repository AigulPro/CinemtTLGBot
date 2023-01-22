from typing import Literal, TypeAlias
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
import json
import requests

import config

Celsius: TypeAlias = float


# Перечисления направлений ветра
class WindDirection(IntEnum):
    North = 0
    Northeast = 45
    East = 90
    Southeast = 135
    South = 180
    Southwest = 225
    West = 270
    Northwest = 315


# Модель получения погоды
@dataclass(slots=True, frozen=True)
class Weather:
    location: str
    temperature: Celsius
    temperature_feeling: Celsius
    description: str
    wind_speed: float
    wind_direction: str
    sunrise: datetime
    sunset: datetime


# Возвращает данные погоды по координатам
def get_weather(coordinates) -> Weather:
    openweather_response = _get_openweather_response(
        longitude=coordinates.lon, latitude=coordinates.lat
    )
    weather = _parse_openweather_response(openweather_response)
    return weather


# Возвращает данные с api до парсинга
def _get_openweather_response(latitude: float, longitude: float) -> str:
    url = config.CURRENT_WEATHER_API_CALL.format(latitude=latitude, longitude=longitude)
    return requests.get(url).text


# Возвращает данные после парсинга
def _parse_openweather_response(openweather_response: str) -> Weather:
    openweather_dict = json.loads(openweather_response)
    return Weather(
        location=_parse_location(openweather_dict),
        temperature=_parse_temperature(openweather_dict),
        temperature_feeling=_parse_temperature_feeling(openweather_dict),
        description=_parse_description(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, 'sunrise'),
        sunset=_parse_sun_time(openweather_dict, 'sunset'),
        wind_speed=_parse_wind_speed(openweather_dict),
        wind_direction=_parse_wind_direction(openweather_dict)
    )


# Возвращает данные на завтра и на 3 и 5 дней
def get_weather_for_next_days(coordinates, days_amoount=1):
    url = config.FIVE_DAYS_WEATHER_API_CALL.format(longitude=coordinates.lon, latitude=coordinates.lat)
    weather_list = json.loads(requests.get(url).text)['list']
    current_day = datetime.now().day
    filter_time = 15

    # Адекватная реализация
    # def filter_date(item):
    #     filter_time = 15
    #     item_date = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
    #     if(current_day == item_date.day and  filter_time == item_date.hour):
    #         return True
    #     else:
    #         current_day = item_date.day
    #         return False
    # print(dict)
    #
    # filtred_dict = filter(filter_date, dict)

    filtred_dict = []
    for item in weather_list:
        item_date = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if current_day == item_date.day and filter_time == item_date.hour:
            filtred_dict.append(item)
        elif current_day != item_date.day:
            current_day = item_date.day

    if days_amoount == 1:
        return filtred_dict[1]
    elif days_amoount == 3:
        del filtred_dict[0]
        del filtred_dict[2:len(filtred_dict)]
    elif days_amoount == 5:
        del filtred_dict[0]

    return filtred_dict


def _parse_location(openweather_dict: dict) -> str:
    return openweather_dict['name']


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return openweather_dict['main']['temp']


def _parse_temperature_feeling(openweather_dict: dict) -> Celsius:
    return openweather_dict['main']['feels_like']


def _parse_description(openweather_dict) -> str:
    return str(openweather_dict['weather'][0]['description']).capitalize()


def _parse_sun_time(openweather_dict: dict, time: Literal["sunrise", "sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_wind_speed(openweather_dict: dict) -> float:
    return openweather_dict['wind']['speed']


# Функция парсинга направления ветра
def _parse_wind_direction(openweather_dict: dict) -> str:
    degrees = openweather_dict['wind']['deg']
    degrees = round(degrees / 45) * 45
    if degrees == 360:
        degrees = 0
    return WindDirection(degrees).name
