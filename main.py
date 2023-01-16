from aiogram import executor

from bot import dp

#запускаем нашего бота, при запуске проекта
if __name__ == '__main__':
    executor.start_polling(dp)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
