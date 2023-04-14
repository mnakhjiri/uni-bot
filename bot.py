import threading
import configparser

import pandas as pd
import telebot

config = configparser.ConfigParser()
config.read('config.ini')
bot = telebot.TeleBot(config['bot']['API_KEY'])

sheet_id = config['bot']['SHEET_ID']
exam_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1143993539"
hw_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"


def get_csv(message, url):
    result = ""
    p = pd.read_csv(url)
    i = 2
    try:
        while True:
            if not isinstance(p.iloc[i, 0], str):
                break
            for j in range(3):
                out = p.iloc[i, j]
                if isinstance(out, str):
                    result += out + " "
            result += "\n\n"
            i += 1
    except Exception as e:
        print(str(e))
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, f"سلام، از این بات می توانید آخرین وضعیت تکالیف و امتحانات را مشاهده نمایید.")


@bot.message_handler(commands=['homeworks'])
def homework(message):
    print("homeworks")
    threading.Thread(target=get_csv, args=(message, hw_url)).start()


@bot.message_handler(commands=['exams'])
def exams(message):
    print("exams")
    threading.Thread(target=get_csv, args=(message, exam_url)).start()


bot.infinity_polling()
