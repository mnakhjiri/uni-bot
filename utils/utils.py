import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import settings
from database import BlackListWord, User

bot = settings.bot

executor = ThreadPoolExecutor(5)


def get_csv(message, url, mode=None):
    from utils.keyboards import homeworkKeyboard
    result = ""
    p = pd.read_csv(url)
    i = 1
    try:
        black_list_words = BlackListWord.get_black_list_words(message.chat.id)
        while True:
            not_show = False
            if not isinstance(p.iloc[i, 0], str):
                continue
            row = ""
            for j in range(3):
                out = p.iloc[i, j]
                if isinstance(out, str):
                    if j != 2:
                        row += out + " | "
                    else:
                        row += out
            for word in black_list_words:
                if word in row:
                    not_show = True
                    break
            if not not_show:
                if mode == "hw":
                    bot.send_message(message.chat.id, row, reply_markup=homeworkKeyboard.get_markup())
                else:
                    result += f"{row}\n\n"
            i += 1
    except IndexError:
        pass
    except Exception as e:
        print(str(e))
    if mode != "hw":
        bot.send_message(message.chat.id, result)


def send_message_to_users(text, users):
    for user in users:
        words = BlackListWord.get_black_list_words(user.chat_id)
        can_send = True
        for word in words:
            if word in text:
                can_send = False
                break
        if can_send:
            try:
                bot.send_message(user.chat_id, text)
            except Exception as e:
                if "bot was blocked by the user" in str(e):
                    User.delete_instance(user)
                else:
                    print(str(e))


def is_admin(chat_id):
    admins = settings.admins
    return str(chat_id) in admins
