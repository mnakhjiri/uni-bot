from database import User, BotLog, database
import settings
from utils.enums import UserActions
from utils.utils import executor


def save_user_to_db(func):
    def wrapper_func(message):
        if message.chat.last_name is None:
            message.chat.last_name = ""
        User.add_user(message.chat.first_name, message.chat.last_name, message.chat.id)
        func(message)

    return wrapper_func


def admin(func):
    def wrapper_func(message):
        admins = settings.admins
        if str(message.chat.id) in admins:
            func(message)

    return wrapper_func


def check_if_ban(func):
    def wrapper_func(message):
        user = User.get(chat_id=message.chat.id)
        if not user.is_ban:
            func(message)
        else:
            settings.bot.send_message(message.chat.id, "این امکان برای شما مسدود است.")

    return wrapper_func


def super_user(func):
    def wrapper_func(message):
        super_user_admin = settings.super_user
        if str(message.chat.id) == super_user_admin:
            func(message)

    return wrapper_func


def save_action(action=None):
    def wrapper_function(func):
        def wrapper(message):
            args = (UserActions.ACTION, message.chat.id)
            if action is not None:
                args = (action, message.chat.id)
            BotLog.add_log(*args)
            # executor.submit(BotLog.add_log, args)
            return func(message)

        return wrapper

    return wrapper_function


def handle_db(func):
    def wrapper(*args, **kwargs):
        database.connect(reuse_if_open=True)
        result = func(*args, **kwargs)
        database.close()
        return result

    return wrapper
