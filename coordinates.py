from urllib.request import urlopen
from dataclasses import dataclass
import json

@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float

# Получение данных по ip
def _get_ip_data() -> dict:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)

# Получение координат из данных
def get_coordinates() -> Coordinates:
    data = _get_ip_data()
    latitude = data['loc'].split(',')[0]
    longitude = data['loc'].split(',')[1]
    print(latitude,longitude)
    return Coordinates(latitude=latitude, longitude=longitude)

