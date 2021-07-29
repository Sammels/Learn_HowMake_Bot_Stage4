# Утилиты
import settings

# Из рандома импортим чойс и рандинт
from random import choice, randint

# Из Емодзи, импортим Эмоджайз
from emoji import emojize

# Импортируем классы для создания клавиатуры.
# (Исп. Питон-ТГ-Бот == 12.6.1 (Новая поломанная))
from telegram import ReplyKeyboardMarkup, KeyboardButton


# Функция для работы со смайлами
def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


# Функция делающая вычисления в игре
def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'Ваше число {user_number}, Моё: {bot_number}. Ты выиграл'
    elif user_number == bot_number:
        message = f'Ваше число {user_number}, Мое {bot_number}, ничья'
    else:
        message = f'Ваше {user_number}, Моеёёё {bot_number}.Моя Чистая победа.'
    return message


# Функция отрисовки клавиатуры
def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Показать котика', KeyboardButton('Мои коорды',request_location=True),
        'Заполнить анкету']
        ])
