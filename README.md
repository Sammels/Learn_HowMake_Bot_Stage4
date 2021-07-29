Телеграмм бот, стадия 4
13.7 Версия сломана кхренам.
инсталим 12.6.1 [socks]
пущай лучше так.

# Работа с диалогами.

Диалог - последовательность Hundler, сообщ системе каким должен быть следующий.


## Новый тип обработчика ConversationHandler
ConversationHandler (Супер Хэндлер) позволяет построить диалог со сложной логикой.
В боте можно использовать несколько таких обработчиков.
У каждого из них своя точка входа и точка выхода.

<b>Как устроен ConverstionHandler</b>

1. `entry_point` - Точка входа запускающая диалог. Список Хэндлеров, и если один из них сработает
то бот начнет обработку данного диалога.

2. `states` - Описывает состояние("Шаги") диалога. У каждого шага есть название и обработчик на которые этот шаг реагирует.

3. `fallback` - Срабатывает когда пользователь вводит что-то неподходящее. Также можно при помощи fallback делать выход из диалога.



## Базовая структура обработчика диалогов

Импортируем `ConversationHandler` и создадим заготовку для нашего диалога - список `entry-points`,
словарь `states`,  и список `fallback`

```
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                              ConversationHandler) 

```

```
anketa = ConversationHandler(
  entry_points = [],
  states={},
  fallbacks=[]
  )

dp.add_handler(anketa)

```


### Создадим отдельный фаил для обработчиков анкеты

Анкета использует несколько обработчиков, и будет расширятся. =>
создадим отдельный файл для неё `anketa.py` 

<h1>Хорошо, когда проект разбит на кусочки, и понятно что в конкретной файле что лежит.</h1>


## Напишем функцию запуска анкеты
<p>Задача функции - убрать основную клавиатуру и определить следующий шаг диалога.
Чтобы сказать боту какой шаг из словаря `states` выполнять мы вернем название шага полностью `return`</p>


```
from telegram import ReplyKeyboardRemove
```
```Python
def anketa_starts(update, context):
  update.message.reply_text(
    "Как вас зовут? Напишите Ваше Имя и Фамилию",
    reply_markup=ReplyKeyboardRemove()
    )
  return "name"
```

После того, как мы стартовали анкету, нужно указать на какой шаг, мы хотим переместиться.


## Вход в диалог

entry_points - список handler, после срабатывания одного из которых диалог будет считаться начатым и бот будет реагировать только на обработчик из этого ConversationHandler:

`from anketa import anketa_starts`

```Python
entry_points=[
      MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_starts)
      ]
```
<b>Добавим в клавиатуру Кнопку "Заполнить анкету"</b>

```Python
def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Показать котика', KeyboardButton('Мои коорды',request_location=True),
        'Заполнить анкету']
        ])
```



# Первый шаг диалога

Состояние (states) диалога, это словарь, где нужный шаг выбирается по ключу.
Давайте добавим ключ "name"

`from anketa import anketa_start, anketa_name`

```Python
states={
  "name": [MessageHandler(Filters.text, anketa_name)]
}
```


## Реализуем функцию anketa_name

```Python
def anketa_name(update, context):
  user_name = update.message.text
  if len(user_name.split()) < 2:
    update.message.reply_text("Пожалуйста напишите имя и фамилию")
    return "name"

  else:
    context.user_data["anketa"] = {"name": user_name}
    reply_keyboard = [["1", "2", "3", "4", "5"]]
    update_message.reply_text(
      "Оцените бота по шкале от 1 до 5",
      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return "raiting"
```


## Получение Пользовательской оценки.
Пользователь может выбрать на клавиатуре оценку от 1 до 5, доавляем регулярное выражение, которое будет реагировать только на эти числа 

`from anketa import anketa_start, anketa_name, anketa_rating`

```Python
states={
  "name": [MessageHandler(Filters.text, anketa_name)],
  "raiting": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)]
}
```

## Последний шаг
### У этого шага будет два обработчика, каждый из котрых будет реализовывать свой функционал

`from anketa import anketa_start, anketa_name, anketa_rating, anketa_comment, anketa_skip`

Добавляем в состояние, комменты + скип.

```Python
states={
  "name": [MessageHandler(Filters.text, anketa_name)],
  "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
  "commment": [
      CommandHandler('skip', anketa_skip),
      MessageHandler(Filters.text, anketa_comment)
      ]
}
```

### Переделка
```Python
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
```

### Добавим fallback

<b>fallback</b> - Хендлер, который отрабатывает при отказе всех остальных хендлеров в диалоге.

`main()`

```Python
fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video| Filters.document, anketa_dontknow)
            ]
```


```Python
# Функция работает когда бот незнает что ему ввел пользователь

def anketa_dontknow(update, context):
    update.message.reply_text("Я вас не понимаю")
```

# Рефакторинг
Рефакторинг - улучшение кода без изменения его пользовательского функционала.
Делается чтобы с кодом было удобно работать, улучшаем дизайн нашего проекта.


# README.md
Документирование проекта - признак его качества.
Самые распространненые форматы Markdown, reStructuredText

# Пример 
# Проект Учебный бот (Главный заголовок)

Учебный бот стадия 4 - это бот для Telegram и показывает пользователю котиков.

## Установка (Заголовок меньше Главного)

1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Впишите в settings.py переменные:
```
API_KEY = "API"
PROXY_URL = "Proxy:port"
PROXY_USERNAME = "Username"
PROXY_PASSWORD = "SuperPassword"
USER_EMOJI = [':smiley_cat:',':smiling_imp:',':panda_face:',':dog:']
``` 
6. Запустите бота коммандой `python3.8 bot3.py`
