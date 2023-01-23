# Клавиатура
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
BTN_GEO = KeyboardButton('🕹 Поделиться Геолокацией', request_location=True)
kb_start.add(BTN_GEO)

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(KeyboardButton('🌞 Сегодня'))
kb_menu.insert(KeyboardButton('🌚 Завтра'))
kb_menu.add(KeyboardButton('📆 На 3 дня'))
kb_menu.insert(KeyboardButton('📆 На 5 дней'))
kb_menu.add(BTN_GEO)

# Клавиатура для получения допольнительной информации на "сегодня"
BTN_SUNRISE = InlineKeyboardButton('Солнце', callback_data='sunrise')
BTN_WIND = InlineKeyboardButton('Ветер', callback_data='wind')

inline_kb = InlineKeyboardMarkup()
inline_kb.add(BTN_SUNRISE)
inline_kb.add(BTN_WIND)

# Клавиатура для получения допольнительной информации на "завтра"
BTN_DOP_TOMORROW = InlineKeyboardButton('Подробнее', callback_data='dop_info')

inline_kb_tommorow = InlineKeyboardMarkup()
inline_kb_tommorow.add(BTN_DOP_TOMORROW)

# Клавиатура для вывода таблицы дополнительный информации на 3 дня
BTN_DOP_MANY_DAYS = InlineKeyboardButton('Подробнее', callback_data='dop_info_table')

inline_kb_many_days = InlineKeyboardMarkup()
inline_kb_many_days.add(BTN_DOP_MANY_DAYS)

# Клавиатура для вывода таблицы дополнительный информации на 5 дня
BTN_DOP_MANY_5DAYS = InlineKeyboardButton('Подробнее', callback_data='dop_info_5table')

inline_kb_many_5days = InlineKeyboardMarkup()
inline_kb_many_5days.add(BTN_DOP_MANY_5DAYS)
