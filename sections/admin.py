from datetime import datetime
from datetime import timedelta
import settings
from database import User, BlackListWord, BotLog
from utils.decorators import save_user_to_db, admin, super_user
from utils import utils
from utils import keyboards

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
@save_user_to_db
@admin
def get_users(message):
    users = User.get_users()
    result = ""
    for user in users:
        result += f"{user.name} {user.last_name}\n"

    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['send_alert_test'])
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


def send_alert_v2(message):
    alert_str = message.text
    users = User.get_users()

    utils.send_message_to_users(alert_str, users)


def send_alert_v2_test(message):
    alert_str = message.text
    users = [User.get(chat_id=message.chat.id)]

    utils.send_message_to_users(alert_str, users)


@bot.message_handler(commands=['admin'])
@save_user_to_db
@admin
def admin_handler(message):
    bot.send_message(message.chat.id, "پنل مدیریت", reply_markup=keyboards.admin_keyboard.get_markup())


@bot.message_handler(commands=['su', 'sudo'])
@super_user
def super_user_handler(message):
    result = ""
    items = list(BotLog.select().where(BotLog.time > datetime.utcnow() - timedelta(minutes=20)).execute())
    for item in items:
        result += f"{item.user.name} {item.user.last_name} {item.action}  {item.time + timedelta(hours=3, minutes=30)}\n\n"
    if result == "":
        bot.send_message(message.chat.id, "nothing to show")
    else:
        bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['unban'])
@super_user
def un_ban(message):
    chat_id = message.text.replace("/unban", "").strip()
    if chat_id == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/unban \nمحتوای پیام")
        return
    User.get(chat_id=chat_id).update(is_ban=False).execute()
    bot.send_message(message.chat.id, "حساب مورد نظر از مسدودیت خارج شد.")


@bot.message_handler(commands=['ban'])
@super_user
def ban(message):
    chat_id = message.text.replace("/ban", "").strip()
    if chat_id == "":
        bot.send_message(message.chat.id, "لظفا پیام خودت به صورت فرمت زیر بفرستید:")
        bot.send_message(message.chat.id, f"/ban \nمحتوای پیام")
        return
    User.get(chat_id=chat_id).update(is_ban=True).execute()
    bot.send_message(message.chat.id, "حساب مورد نظر مسدود شد.")