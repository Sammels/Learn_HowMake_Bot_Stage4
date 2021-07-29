# Бот версия 4 (Может даже переработка)

# Импортируем логгирование и преднастройка
import logging
import settings

# Персональная импортирование
from handlers import (greet_user, talk_to_me, guess_number, send_cat_picture,
                      user_coordinates)

# Импортируем начало анкеты, из модуля анкеты.
from anketa import (anketa_start, anketa_name, anketa_rating, anketa_comment,
                   anketa_skip, anketa_dontknow)

# Импортим из либы тг: Апдейтер, CommandHandler, MessageHandler, Filters
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Логгирование сообщений в файл bot4.log, level=logging.INFO
logging.basicConfig(filename='bot4.log', level=logging.INFO)

# Cоздаем словарь с проксей-сервером
PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                  'password': settings.PROXY_PASSWORD}}


# Функции для запуска ТГ бота
def main():
    # Создаем ТГ боты, и передаем Апишку для работы
    mybot4 = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    # Используем Диспетчер mybot4.dispatcher
    # чтобы при наступлении события вызывалась наша функция
    dp = mybot4.dispatcher

    # Делаем ConversationHandler (Общенииииее) создавая анкету
    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'),
                           anketa_start)],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'),
                                      anketa_rating)],
            "comment": [
                CommandHandler('skip', anketa_skip),
                MessageHandler(Filters.text, anketa_comment)
                ]
            },
        fallbacks=[
            MessageHandler(Filters.text|Filters.photo|Filters.video|Filters.document|Filters.location,
                          anketa_dontknow)
            ]
        )

    # Добавляем сам обработчик
    dp.add_handler(anketa)

    # Добавляем обработчик, реагирующий на /start и вызывать функцию
    dp.add_handler(CommandHandler("start", greet_user))

    # Обработчик команды guess. Игра больше меньше.
    dp.add_handler(CommandHandler("guess", guess_number))

    # Обработчик команды cat. Картинка с котиками
    dp.add_handler(CommandHandler("cat", send_cat_picture))

    # Добавим обработчик реагирующий на строку "Показать котиков"
    dp.add_handler(MessageHandler(Filters.regex('^(Показать котика)$'),
                                  send_cat_picture))

    # Добавим обработчик координат
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))

    # Добавим обработчик, реагирующий на текстове сообщение
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # Запись "Бот стартовал", Логгирование
    logging.info("Бот стартовал!")

    # Отравляем бота в ТГ за сообщениями
    mybot4.start_polling()

    # Запускаем бота. Работает до принудительной остановки.
    mybot4.idle()


# Если этот файл вызвали python3 bot4.py
# то будет вызван main
# если нет, то main вызван не будет.
if __name__ == '__main__':
    main()
