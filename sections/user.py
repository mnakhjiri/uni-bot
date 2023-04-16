import threading

from utils import utils
from utils.decorators import *
from database import *

bot = settings.bot


@bot.message_handler(commands=['start'])
@save_user_to_db
def greet(message):
    bot.send_message(message.chat.id, f"سلام، از این بات می توانید آخرین وضعیت تکالیف و امتحانات را مشاهده نمایید.")


@bot.message_handler(commands=['homeworks'])
@save_user_to_db
def homework(message):
    threading.Thread(target=utils.get_csv, args=(message, settings.hw_url)).start()


@bot.message_handler(commands=['exams'])
@save_user_to_db
def exams(message):
    threading.Thread(target=utils.get_csv, args=(message, settings.exam_url)).start()


@bot.message_handler(commands=['id'])
@save_user_to_db
def get_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))


@bot.message_handler(commands=['feedback'])
@save_user_to_db
def send_feedback(message):
    feedback_str = message.text.replace("/feedback", "")
    if feedback_str == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/feedback \nمحتوای پیام")
        return
    admins = settings.config['bot']['ADMIN_IDS'].split(",")
    bot.forward_message(admins[0], message.chat.id, message.id)


@bot.message_handler(commands=['sheet'])
@save_user_to_db
def send_sheet(message):
    bot.send_message(message.chat.id, settings.sheet_url)


@bot.message_handler(commands=['dont_show'])
@save_user_to_db
def dont_show_word(message):
    black_word = message.text.replace("/dont_show", "").strip()
    if black_word == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/dont_show \nمحتوای پیام")
        return
    BlackListWord.add_to_black_list(black_word, message.chat.id)
    bot.send_message(message.chat.id, "عبارت مورد نظر از این به بعد نمایش داده نمی شود.")


@bot.message_handler(commands=['show'])
@save_user_to_db
def show_word(message):
    black_word = message.text.replace("/show", "").strip()
    if black_word == "":
        bot.send_message(message.chat.id, "لطفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/show \nمحتوای پیام")
        return
    BlackListWord.remove_from_black_list(black_word, message.chat.id)
    bot.send_message(message.chat.id, "عبارت مورد نظر از این به بعد نمایش داده می شود.")


@bot.message_handler(commands=['hidden_words'])
@save_user_to_db
def show_blacklist(message):
    words = BlackListWord.get_black_list_words(message.chat.id)
    out = ""
    for word in words:
        out += f"{word}\n"
    if out == "":
        bot.send_message(message.chat.id, "شما عبارتی در لیست پنهان ندارید.")
    else:
        bot.send_message(message.chat.id, out)


@bot.message_handler(commands=['reset_hidden_words'])
@save_user_to_db
def reset_blacklist(message):
    BlackListWord.remove_all_black_list(message.chat.id)
    bot.send_message(message.chat.id, "تمامی عبارات از لیست پنهان حذف شدند.")


@bot.message_handler(commands=['cancel'])
def cancel_session(message):
    session = Session.get_or_none(user=User.get(chat_id=message.chat.id))
    if session is not None:
        Session.delete_instance(session)
        bot.send_message(message.chat.id, "عملیات مورد نظر کنسل شد.")
    else:
        pass
