import threading
import configparser
from database import *
import pandas as pd
import telebot

config = configparser.ConfigParser()
config.read('config.ini')
bot = telebot.TeleBot(config['bot']['API_KEY'])

sheet_id = config['bot']['SHEET_ID']
exam_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1143993539"
hw_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"


# decorators


def save_user_to_db(func):
    def wrapper_func(message):
        if message.chat.last_name is None:
            message.chat.last_name = ""
        User.add_user(message.chat.first_name, message.chat.last_name, message.chat.id)
        func(message)

    return wrapper_func


# base bot
def get_csv(message, url):
    result = ""
    p = pd.read_csv(url)
    i = 2
    try:
        while True:
            if not isinstance(p.iloc[i, 0], str):
                continue
            for j in range(3):
                out = p.iloc[i, j]
                if isinstance(out, str):
                    result += out + " "
            result += "\n\n"
            i += 1
    except IndexError:
        pass
    except Exception as e:
        print(str(e))
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['start'])
@save_user_to_db
def greet(message):
    bot.send_message(message.chat.id, f"سلام، از این بات می توانید آخرین وضعیت تکالیف و امتحانات را مشاهده نمایید.")


@bot.message_handler(commands=['homeworks'])
@save_user_to_db
def homework(message):
    print("homeworks")
    threading.Thread(target=get_csv, args=(message, hw_url)).start()


@bot.message_handler(commands=['exams'])
@save_user_to_db
def exams(message):
    print("exams")
    threading.Thread(target=get_csv, args=(message, exam_url)).start()


@bot.message_handler(commands=['test'])
def test(message):
    users = User.get_users()
    for user in users:
        print(user.name, user.chat_id)


bot.infinity_polling()
