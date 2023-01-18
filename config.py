# наш токен доступа к API телеграмма
TOKEN_API_TELEGRAM = "5979613899:AAFAyxfJmy-pl2RVOI1q9nkNooBsf8GmzZU"
TOKEN_API_WEATHER = "6c06cce7d63081151f29f7af1fe4bf97"

CURRENT_WEATHER_API_CALL = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={latitude}&lon={longitude}&'
        'appid=' + TOKEN_API_WEATHER + '&units=metric'
)
