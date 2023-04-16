import pandas as pd

import settings
from database import BlackListWord, User

bot = settings.bot


def get_csv(message, url):
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
                    row += out + " "
            for word in black_list_words:
                if word in row:
                    not_show = True
                    break
            if not not_show:
                result += f"{row}\n\n"
            i += 1
    except IndexError:
        pass
    except Exception as e:
        print(str(e))
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
