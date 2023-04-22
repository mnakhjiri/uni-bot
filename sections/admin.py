from datetime import datetime
from datetime import timedelta
import settings
from database import User, BlackListWord, BotLog, UserCustomConfigs
from utils.decorators import save_user_to_db, admin, super_user, handle_db
from utils import utils
from utils import keyboards
from utils.enums import *

bot = settings.bot


@bot.message_handler(commands=['status'])
@save_user_to_db
@admin
def status(message):
    number_of_users = User.select().count()
    result = ""
    number_of_blacklist_words = BlackListWord.select().group_by(BlackListWord.text).count()
    number_of_users_using_blacklist_words = BlackListWord.select().group_by(BlackListWord.user).count()
    result += f"{'تعداد کاربران'} : {number_of_users}\n\n"
    result += f"{'تعداد کلمه های در لیست سیاه'} : {number_of_blacklist_words}\n\n"
    result += f"{'تعداد کاربر هایی که از فیلتر پنهان استفاده میکنند'} : {number_of_users_using_blacklist_words}"
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['users'])
@handle_db
@save_user_to_db
@admin
def get_users(message):
    users = User.get_users()
    result = ""
    if str(message.chat.id) == settings.super_user:
        for user in users:
            if user.is_ban:
                result += f"{user.name} {user.last_name} {user.chat_id}  Banned User**\n"
            else:
                result += f"{user.name} {user.last_name} {user.chat_id}\n"
    else:
        for user in users:
            result += f"{user.name} {user.last_name}\n"

    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['send_alert_test'])
@handle_db
@save_user_to_db
@admin
def send_alert_test(message):
    alert_str = message.text.replace("/send_alert_test", "")
    if alert_str == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/send_alert_test \nمحتوای پیام")
        return
    user = User.get(chat_id=message.chat.id)
    utils.send_message_to_users(alert_str, [user])


@bot.message_handler(commands=['send_alert'])
@handle_db
@save_user_to_db
@admin
def send_alert(message):
    alert_str = message.text.replace("/send_alert", "")
    if alert_str == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/send_alert \nمحتوای پیام")
        return
    users = User.get_users()
    utils.send_message_to_users(alert_str, users)


@handle_db
def send_alert_v2(message):
    alert_str = message.text
    users = User.get_users()

    utils.send_message_to_users(alert_str, users)


@handle_db
def send_alert_v2_test(message):
    alert_str = message.text
    users = [User.get(chat_id=message.chat.id)]

    utils.send_message_to_users(alert_str, users)


@bot.message_handler(commands=['admin'])
@handle_db
@save_user_to_db
@admin
def admin_handler(message):
    bot.send_message(message.chat.id, "پنل مدیریت", reply_markup=keyboards.admin_keyboard.get_markup())


@bot.message_handler(commands=['su', 'sudo'])
@handle_db
@super_user
def super_user_handler(message):
    result = ""
    items = list(BotLog.select().where(BotLog.time > datetime.utcnow() - timedelta(minutes=20)).execute())
    items2 = list(BotLog.select().where(BotLog.time > datetime.utcnow() - timedelta(days=1)).execute())
    items3 = list(BotLog.select().where(BotLog.time > datetime.utcnow() - timedelta(days=3)).execute())

    users_set = set()
    users_set_three = set()
    for item in items2:
        users_set.add(item.user)
    for item in items3:
        users_set_three.add(item.user)
    for item in items:
        result += f"{item.user.name} {item.user.last_name} {item.action}  {item.time + timedelta(hours=3, minutes=30)}\n\n"
    if result == "":
        bot.send_message(message.chat.id, "nothing to show")
    else:
        bot.send_message(message.chat.id, result)
    bot.send_message(message.chat.id, f"Number of users used the bot in the last 24 hours : {len(users_set)}")
    bot.send_message(message.chat.id, f"Number of users used the bot in the last 72 hours : {len(users_set_three)}")


@bot.message_handler(commands=['unban'])
@handle_db
@super_user
def un_ban(message):
    chat_id = message.text.replace("/unban", "").strip()
    if chat_id == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/unban \nمحتوای پیام")
        return
    user = User.get(chat_id=chat_id)
    user.is_ban = False
    user.save()
    bot.send_message(message.chat.id, "حساب مورد نظر از مسدودیت خارج شد.")


@bot.message_handler(commands=['ban'])
@handle_db
@super_user
def ban(message):
    chat_id = message.text.replace("/ban", "").strip()
    if chat_id == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/ban \nمحتوای پیام")
        return
    user = User.get(chat_id=chat_id)
    user.is_ban = True
    user.save()
    bot.send_message(message.chat.id, "حساب مورد نظر مسدود شد.")
