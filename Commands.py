from telegram.ext import CommandHandler
from random import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyowm import OWM
from pyowm.utils.config import get_default_config


reply_keyboard1 = [['/dice', '/timer'],
                  ['/close_keyboard']]
reply_keyboard2 = [['/six_cube', '/two_six_cube'],
                  ['/twenty_cube']]
reply_keyboard3 = [['/set_timer 30', '/set_timer 60'],
                  ['/set_timer 350', '/unset_timer']]

markup = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True)
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)


def register(update, context):
    update.message.reply_text('Скоро')


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def start(update, context):
    update.message.reply_text(
        "Здравствуйте! Я Бот-помощник для повседневной жизни. Чтобы узнать, что я могу, используйте команду /help")


def timer(update, context):
    update.message.reply_text('Команды раздела timer:\n'
                              '/set_timer <секунд> - засечь таймер\n'
                              '/unset_timer - удалить действующий таймер\n', reply_markup=markup3)


def dice(update, context):
    update.message.reply_text('Команды раздела dice:\n'
                              '/six_cube - бросить один шестигранный кубик\n'
                              '/two_six_cube - бросить два шестигранных кубика\n'
                              '/twenty_cube - бросить двадцатигранный кубик\n', reply_markup=markup2)


def six_cube(update, context):
    update.message.reply_text(f'Вы бросили шестигранный кубик, вам выпало число {randint(1, 6)}')


def two_six_cube(update, context):
    update.message.reply_text(f'Вы бросили два шестигранных кубика, вам выпали числа {randint(1, 6)} и {randint(1, 6)}')


def twenty_cube(update, context):
    update.message.reply_text(f'Вы бросили двадцатигранный кубик, вам выпало число {randint(1, 20)}')


def weather(update, context):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM('cbadeffbd8b053d2915c4b213e8fd515', config_dict)
    mgr = owm.weather_manager()

    citi = open('data/cities.txt', mode='r', encoding='utf-8')
    data1 = citi.read()
    cities = data1.split(', ')
    try:
        place = context.args[0]
        if place not in cities:
            update.message.reply_text('Ошибка, проверьте правильность названия города.\n'
                                        'Пример использования: /weather Ростов-на-Дону')
        else:
            observation = mgr.weather_at_place(place)
            w = observation.weather
            t = w.temperature("celsius")
            t1 = t['temp']
            t2 = t['feels_like']
            wind = w.wind()['speed']
            humi = w.humidity
            press = w.pressure['press']
            dt = w.detailed_status
            update.message.reply_text("В городе " + str(place) + " температура " + str(t1) + " °C.\n"
                "Ощущается как " + str(t2) + " °C.\n"
                "Скорость ветра: " + str(wind) + " м/с.\n"
                "Влажность: " + str(humi) + " %.\n"
                "Давление: " + str(press) + " мм.рт.ст.\n"
                "Осадки: " + str(dt))
    except:
        update.message.reply_text('Ошибка, Вы не ввели город.\n'
                                  'Пример использования: /weather Москва')


def menu(update, context):
    update.message.reply_text('/dice\n'
                              '/six_cube\n'
                              '/two_six_cube\n'
                              '/twenty_cube\n'
                              '/timer\n'
                              '/set_timer 10\n'
                              '/unset_timer\n'
                              '/weather Ростов-на-Дону\n'
                              '/close_keyboard', reply_markup=markup)


def help(update, context):
    update.message.reply_text('Информация о том, что и какая команда делает:\n'
                              '/dice - раздел, где можно испытать удачу\n'
                              '/timer - раздел, где можно управлять временем\n'
                              '/weather - раздел, где можно узнать о погоде\n'
                              '/menu - открывает все команды\n'
                              '/close_keyboard - удаляет действующую клавиатуру', reply_markup=markup)


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text='Время вышло!')


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер удалён.' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Ошибка, нельзя задавать отричательные значения.')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Напишу вам, когда пройдёт {due} секунд.'
        if job_removed:
            text += '\nСтарый таймер удалён.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_timer <секунд>')


menu_command = CommandHandler('menu', menu)
weather_command = CommandHandler('weather', weather)
register_command = CommandHandler('register', register)
start_command = CommandHandler('start', start)
help_command = CommandHandler('help', help)
dice_command = CommandHandler('dice', dice)
timer_command = CommandHandler('timer', timer)
six_cube_command = CommandHandler('six_cube', six_cube)
two_six_cube_command = CommandHandler('two_six_cube', two_six_cube)
twenty_cube_command = CommandHandler('twenty_cube', twenty_cube)