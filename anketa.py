# Создаем анкету которая используется в 4.py > main()

# Импортируем модуль, чтобы убрать клавиатуру
from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Импортируем модуль для завершения диалога.
from telegram.ext import ConversationHandler

# Покажем пользователю клавиатуру
from utills import main_keyboard


# Функция начала анкеты
def anketa_start(update, context):
    update.message.reply_text(
        "Как вас зовут? Напишите Ваше Имя и Фамилию",
        reply_markup=ReplyKeyboardRemove()
        )
    return "name"


# Функция принимающая Имя анкетируемого
def anketa_name(update, context):
    user_name = update.message.text
# Если что-то меньше двух слов, повторно (сплит разделение по пробелам)
    if len(user_name.split()) < 2:
        update.message.reply_text("Пожалуйста напишите имя и фамилию")
        return "name"

    else:
    # Хранилище где мы можем схранять данные о конкретном пользователе.
        context.user_data["anketa"] = {"name": user_name}

    # Делаем клавиатуру, чтобы пользователю было удобно оценивать
        reply_keyboard = [["1", "2", "3", "4", "5"]]

    # Пишем пользователю ответ
        update.message.reply_text(
          "Оцените бота по шкале от 1 до 5",

    # Эта клавиатура будет показана 1 раз
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return "rating"


# Функция анкеты рейтинга
def anketa_rating(update, context):
    context.user_data['anketa']['rating'] = int(update.message.text)
    update.message.reply_text("Напишите комментарий или нажмите /skip чтобы пропустить.")
    return "comment"

# Функция комментариев в анкете
def anketa_comment(update, context):
    # Принимаем от пользователя его коммент и сохраняем.
    context.user_data['anketa']['comment'] = update.message.text

    # Создадим текст который будем отправлять пользователю
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)

    # Завершаем диалог
    return ConversationHandler.END


# Функция пропуска 
def anketa_skip(update, context):
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)

    # Завершаем диалог
    return ConversationHandler.END


# Функция форматирования
def format_anketa(anketa):
    user_text = f"""<b>Имя Фамилия</b>: {anketa['name']}
<b>Оценка</b>: {anketa['rating']}
"""
    if 'comment' in anketa:
        user_text += f"\n<b>Комментарий</b>: {anketa['comment']}"
    return user_text


# Функция работает когда бот незнает что ему ввел пользователь

def anketa_dontknow(update, context):
    update.message.reply_text("Я вас не понимаю")