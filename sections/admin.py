import settings
from database import User, BlackListWord
from utils.decorators import save_user_to_db, admin
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
    result += f"number_of_users : {number_of_users}\n\n"
    result += f"number_of_blacklist_words : {number_of_blacklist_words}\n\n"
    result += f"number_of_users_using_blacklist_words : {number_of_users_using_blacklist_words}"
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['users'])
@save_user_to_db
@admin
def get_users(message):
    users = User.get_users()
    result = ""
    for user in users:
        result += f"{user.name} {user.last_name} : {user.chat_id}\n"

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


@bot.message_handler(commands=['test'])
@save_user_to_db
@admin
def test(message):
    bot.send_message(message.chat.id, "Hello", reply_markup=keyboards.test.get_markup())
