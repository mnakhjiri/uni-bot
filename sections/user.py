import threading
from datetime import timedelta

from utils import utils
from utils.decorators import *
from database import *
from utils import keyboards
from utils.enums import *

bot = settings.bot


@bot.message_handler(commands=['start'])
@handle_db
@save_user_to_db
@save_action(action=UserActions.START_BOT)
def greet(message):
    bot.send_message(message.chat.id, f"سلام، از این بات می توانید آخرین وضعیت تکالیف و امتحانات را مشاهده نمایید.")


@bot.message_handler(commands=['homeworks'])
@handle_db
@save_user_to_db
@save_action(action=UserActions.SEND_HW)
def homework(message):
    threading.Thread(target=utils.get_csv, args=(message, settings.hw_url, "hw")).start()


@bot.message_handler(commands=['exams'])
@handle_db
@save_user_to_db
@save_action(action=UserActions.SEND_EXAMS)
def exams(message):
    threading.Thread(target=utils.get_csv, args=(message, settings.exam_url)).start()


@bot.message_handler(commands=['id'])
@handle_db
@save_user_to_db
@save_action(action=UserActions.SEND_ID)
def get_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))


@bot.message_handler(commands=['feedback'])
@handle_db
@save_user_to_db
@save_action(action=UserActions.SEND_FEEDBACK)
def send_feedback(message):
    feedback_str = message.text.replace("/feedback", "")
    if feedback_str == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/feedback \nمحتوای پیام")
        return
    admins = settings.config['bot']['ADMIN_IDS'].split(",")
    bot.forward_message(admins[0], message.chat.id, message.id)


@bot.message_handler(commands=['sheet'])
@handle_db
@save_user_to_db
@save_action(action=UserActions.SEND_SHEET)
def send_sheet(message):
    bot.send_message(message.chat.id, settings.sheet_url)


@handle_db
@save_user_to_db
@save_action(action=UserActions.DONT_SHOW)
def dont_show_word_v2(message):
    black_word = message.text
    BlackListWord.add_to_black_list(black_word, message.chat.id)
    bot.send_message(message.chat.id, "عبارت مورد نظر از این به بعد نمایش داده نمی شود.")


@handle_db
@save_user_to_db
@save_action(action=UserActions.SHOW_WORD)
def show_word_v2(message):
    black_word = message.text
    BlackListWord.remove_from_black_list(black_word, message.chat.id)
    bot.send_message(message.chat.id, "عبارت مورد نظر از این به بعد نمایش داده می شود.")


@handle_db
@save_user_to_db
@save_action(action=UserActions.SEND_FILTERED_WORDS)
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
@handle_db
@save_action(action=UserActions.SHOW_FILTERED_PANEL)
def show_hidden_keyboard(message):
    bot.send_message(message.chat.id, "مدیریت عبارات فیلتر شده",
                     reply_markup=keyboards.user_keyboard_hidden_words.get_markup())


@handle_db
@save_user_to_db
@save_action(action=UserActions.RESET_BLACKLIST)
def reset_blacklist_v2(message):
    BlackListWord.remove_all_black_list(message.chat.id)
    bot.send_message(message.chat.id, "تمامی عبارات از لیست پنهان حذف شدند.")


@bot.message_handler(commands=['cancel'])
@handle_db
@save_action(action=UserActions.CANCEL_SESSION)
def cancel_session(message):
    session = Session.get_or_none(user=User.get(chat_id=message.chat.id))
    if session is not None:
        Session.delete_instance(session)
        bot.send_message(message.chat.id, "عملیات مورد نظر کنسل شد.")
    else:
        pass


@bot.message_handler(commands=["filter_poll"])
@handle_db
@save_action(action=UserActions.SEND_POLL)
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


@bot.message_handler(commands=["food"])
@handle_db
@save_action(action=UserActions.FOOD)
@check_if_ban
def food(message):
    message_str = "تبادل کد فراموشی (آزمایشی)"
    message_str += "\n مقررات: " + "\n\n"
    message_str += "در صورت دریافت  گزارش تخلف بن خواهید شد." + "\n\n"
    message_str += "فقط نام غذای خود را به اشتراک بگذارید کد را در بات ارسال نکنید" + "\n\n"
    message_str += "در صورت گزارش دریافت بیش از ۳ غذا در یک روز بن خواهید شد" + "\n\n"
    bot.send_message(message.chat.id, message_str, reply_markup=keyboards.foodKeyboard.get_markup())


@handle_db
@check_if_ban
def send_foods(message):
    try:
        to_user = User.get(chat_id=message.chat.id)
        user_foods = list(
            FoodCode.select().where(FoodCode.time_created > datetime.utcnow() - timedelta(hours=6),
                                    FoodCode.to_user == to_user).execute())
    except AttributeError:
        bot.send_message(message.chat.id, "غذایی در لیست امروز ثبت نشده است.")
        return
    if len(user_foods) > 3:
        if str(message.chat.id) != str(settings.super_user):
            user = User.get(chat_id=message.chat.id)
            user.is_ban = True
            user.save()
            bot.send_message(message.chat.id, "به دلیل دریافت تعداد بیش از حد کد فراموشی حساب شما بن شد.")
            return
    foods = list(
        FoodCode.select().where(FoodCode.time_created > (datetime.utcnow() - timedelta(days=1))).execute())

    if len(foods) == 0:
        bot.send_message(message.chat.id, "غذایی در لیست امروز اضافه نشده است.")
        return
    sent = False
    for food_item in foods:
        if food_item.to_user is None:
            bot.send_message(message.chat.id, f"{food_item.id} | {food_item.desc}",
                             reply_markup=keyboards.getFoodKeyboard.get_markup())
            sent = True
    if not sent:
        bot.send_message(message.chat.id, "تمامی غذا ها تبادل شده اند")


@handle_db
@bot.poll_answer_handler()
# @save_action(action=UserActions.ANSWER_POLL)
def handle_poll(poll):
    courses = settings.poll_answer_options
    for i in range(len(courses)):
        if courses[i] == "...":
            continue
        if i in poll.option_ids:
            BlackListWord.add_to_black_list(courses[i], poll.user.id)
        else:
            BlackListWord.remove_from_black_list(courses[i], poll.user.id)
    bot.send_message(poll.user.id, "فیلتر مورد نظر با موفقیت اعمال شد")


@bot.message_handler(commands=["show_alerts"])
@handle_db
@save_action(action=UserActions.SHOW_ALERTS)
def show_alerts(message):
    user_config = UserCustomConfigs.get_or_none(user=User.get(chat_id=message.chat.id),
                                                custom_config_mode=UserCustomConfigsEnum.DONT_SHOW_ALERTS.value)
    if user_config is not None:
        UserCustomConfigs.delete_instance(user_config)
    bot.send_message(message.chat.id, "اطلاعیه ها از این به بعد نمایش داده می شوند.")
