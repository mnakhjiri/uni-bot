from database import User
import settings


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
