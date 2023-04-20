import threading

from utils import utils
from utils.decorators import *
from database import *
from utils import keyboards

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


@save_user_to_db
def dont_show_word_v2(message):
    black_word = message.text
    BlackListWord.add_to_black_list(black_word, message.chat.id)
    bot.send_message(message.chat.id, "عبارت مورد نظر از این به بعد نمایش داده نمی شود.")


@save_user_to_db
def show_word_v2(message):
    black_word = message.text
    BlackListWord.remove_from_black_list(black_word, message.chat.id)
    bot.send_message(message.chat.id, "عبارت مورد نظر از این به بعد نمایش داده می شود.")


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


@bot.message_handler(commands=['hidden_words'])
def show_hidden_keyboard(message):
    bot.send_message(message.chat.id, "مدیریت عبارات فیلتر شده",
                     reply_markup=keyboards.user_keyboard_hidden_words.get_markup())


@save_user_to_db
def reset_blacklist_v2(message):
    BlackListWord.remove_all_black_list(message.chat.id)
    bot.send_message(message.chat.id, "تمامی عبارات از لیست پنهان حذف شدند.")


@bot.message_handler(commands=['cancel'])
@save_action
def cancel_session(message, action=UserActions.CANCEL_SESSION):
    session = Session.get_or_none(user=User.get(chat_id=message.chat.id))
    if session is not None:
        Session.delete_instance(session)
        bot.send_message(message.chat.id, "عملیات مورد نظر کنسل شد.")
    else:
        pass


@bot.message_handler(commands=["filter_poll"])
def create_poll(message):
    bot.send_message(message.chat.id, "درس هایی که نمی خواهید در ددلاین ها برای شما نمایش داده شوند را انتخاب کنید")
    answer_options = settings.poll_answer_options[:]
    extra_items = []
    while len(answer_options) > 10:
        extra_items.append(answer_options.pop())
    bot.send_poll(
        chat_id=message.chat.id,
        question="درس هایی که می خواهید فیلتر بشوند : ",
        options=answer_options,
        type="regular",
        allows_multiple_answers=True,
        is_anonymous=False,
    )
    answer = ""
    for item in extra_items:
        answer += f"({item})\n"
    if answer != "":
        answer = "به دلیل محدودیت تلگرام در ارسال poll موارد زیر ارسال نشد. لطفا در  صورت تمایل در بخش فیلتر کردن گزارش ها آن را تغییر بدهید." + "\n\n" + answer
        bot.send_message(message.chat.id, answer)


@bot.poll_answer_handler()
@save_action
def handle_poll(poll, action=UserActions.ANSWER_POLL):
    courses = settings.poll_answer_options
    for i in range(len(courses)):
        if courses[i] == "...":
            continue
        if i in poll.option_ids:
            BlackListWord.add_to_black_list(courses[i], poll.user.id)
        else:
            BlackListWord.remove_from_black_list(courses[i], poll.user.id)
    bot.send_message(poll.user.id, "فیلتر مورد نظر با موفقیت اعمال شد")
