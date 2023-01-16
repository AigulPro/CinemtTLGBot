import time
import logging
import config

from aiogram import Bot, Dispatcher, types,executor

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot)


#обработчик который обрабатывает команду start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    #Логируем
    user = message.from_user.id
    user_full_name = message.from_user.username
    logging.info(f'{user}_{user_full_name}_{time.asctime()}')
    #Возвращаем ответ
    await message.reply('Привет, ебать я работаю!')

