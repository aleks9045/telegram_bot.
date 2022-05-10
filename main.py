# Название бота: @Yandex_python_bot
from telegram.ext import Updater
from Commands import *


TOKEN = '5154036804:AAGiZKNNRLEspsSnWddVP_C85qIaJxIKUcw'


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(two_six_cube_command)
    dp.add_handler(twenty_cube_command)
    dp.add_handler(six_cube_command)
    dp.add_handler(timer_command)
    dp.add_handler(dice_command)
    dp.add_handler(register_command)
    dp.add_handler(start_command)
    dp.add_handler(help_command)
    dp.add_handler(weather_command)
    dp.add_handler(menu_command)

    dp.add_handler(CommandHandler("close_keyboard", close_keyboard))
    dp.add_handler(CommandHandler("set_timer", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset_timer", unset_timer,
                                  pass_chat_data=True)
                   )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
