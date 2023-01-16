import time
import logging
from . import config

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handlers(commands=['/start'])
async def start_bot(message: types.Message):
    #Логируем
    user = message.from_user.id
    user_full_name = message.from_user.username
    logging.INFO(f'{user}_{user_full_name}_{time.asctime()}')
    #Возвращаем ответ
    await message.reply('Привет, ебать я работаю!')
