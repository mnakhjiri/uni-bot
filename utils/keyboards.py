from datetime import datetime, timedelta

import telebot

import sections.user
from utils.decorators import handle_db
from utils.enums import AdminSessionStates, UserSessionStates, UserCustomConfigsEnum
import database
import settings
from sections import admin

bot = settings.bot


class BaseInlineKeyboard:
    def __init__(self, keyboard_buttons, unique_id=0, row_width=1, prev_markup=None, next_states=None):
        self.keyboard_buttons = keyboard_buttons
        self.unique_id = unique_id
        self.row_width = row_width
        self.prev_markup = prev_markup
        self.next_states = next_states

    def get_markup(self):
        result = telebot.types.InlineKeyboardMarkup(row_width=self.row_width)
        keyboards = self.keyboard_buttons
        for keyboard in keyboards:
            result.add(keyboard)
        if self.prev_markup is not None:
            result.add(self.prev_markup)
        return result

    def do_action(self, action: str, message):
        print("fail")
        pass


class AdminKeyboard(BaseInlineKeyboard):
    @handle_db
    def do_action(self, action: str, message):
        if action == "status":
            admin.status(message)
        elif action == "getUsers":
            admin.get_users(message)
        elif action == "alert":
            bot.send_message(message.chat.id, "لطفا متن اطلاعیه را وارد نمایید. برای انصراف /cancel را ارسال نمایید.")
            database.Session.create_session(message.chat.id, AdminSessionStates.WAITING_TO_SEND_ALERT)
        elif action == "alertTest":
            bot.send_message(message.chat.id,
                             "لطفا متن اطلاعیه آزمایشی را وارد نمایید. برای انصراف /cancel را ارسال نمایید.")
            database.Session.create_session(message.chat.id, AdminSessionStates.WAITING_TO_SEND_TEST_ALERT)


class UserKeyboardHiddenWords(BaseInlineKeyboard):

    @handle_db
    def do_action(self, action: str, message):
        if action == "view":
            sections.user.show_blacklist(message)
        elif action == "show":
            bot.send_message(message.chat.id,
                             "لطفا عبارت خود را برای نمایش در گزارشات وارد نمایید. برای انصراف /cancel را ارسال نمایید.")
            database.Session.create_session(message.chat.id, UserSessionStates.WAITING_TO_SEND_SHOW_WORD)
        elif action == "dontshow":
            bot.send_message(message.chat.id,
                             "لطفا عبارت خود را برای عدم نمایش در گزارشات وارد نمایید. برای انصراف /cancel را ارسال نمایید.")
            database.Session.create_session(message.chat.id, UserSessionStates.WAITING_TO_SEND_DONT_SHOW_WORD)
        elif action == "reset":
            sections.user.reset_blacklist_v2(message)


class HomeworkKeyboard(BaseInlineKeyboard):

    @handle_db
    def do_action(self, action: str, message):
        if action == "done":
            database.BlackListWord.add_to_black_list(message.text.split("|")[0].strip(), message.chat.id)
            bot.delete_message(message.chat.id, message.message_id)


class GetFoodKeyboard(BaseInlineKeyboard):

    @handle_db
    def do_action(self, action: str, message):
        if action == "getFood":
            if database.User.get(chat_id=message.chat.id).is_ban:
                bot.send_message(message.chat.id, "حساب کاربری شما بن شده است.")
                return
            food_id = message.text.split("|")[0].strip()
            result = database.FoodCode.get_food_code(message.chat.id, food_id)
            if not result:
                bot.send_message(message.chat.id, "کد مورد نظر ارسال نشد. احتمالا کسی قبل شما آن را گرفته است.")
            else:
                bot.send_message(message.chat.id,
                                 f"   برای دریافت کد به id زیر پیغام بدهید :  ")
                chat = settings.bot.get_chat(result)
                to_user_chat = settings.bot.get_chat(message.chat.id)
                if to_user_chat.username is not None:
                    bot.send_message(result, f"کاربر زیر غذای شما را دریافت کرد:")
                    bot.send_message(result, f"@{to_user_chat.username}")
                else:
                    name = to_user_chat.first_name
                    last_name = to_user_chat.last_name
                    if last_name is None:
                        last_name = ""
                    bot.send_message(result, f"کاربر زیر غذای شما را دریافت کرد:")
                    bot.send_message(result, f"{name} {last_name}")
                if chat.username is None:
                    bot.send_message(message.chat.id, f"tg://openmessage?user_id={result}")
                else:
                    bot.send_message(message.chat.id, f"@{chat.username}")


class FoodKeyboard(BaseInlineKeyboard):

    @handle_db
    def do_action(self, action: str, message):
        if action == "sendFoods":
            sections.user.send_foods(message)
        if action == "shareFood":
            if database.User.get(chat_id=message.chat.id).is_ban:
                bot.send_message(message.chat.id, "حساب کاربری شما بن شده است.")
                return
            chat = settings.bot.get_chat(message.chat.id)
            if chat.username is None:
                alert_message = "شما username ندارید و در صورت تبادل chat_id شما به اشتراک گذاشته می شود. آیا موافقید؟"
                bot.send_message(message.chat.id, alert_message, reply_markup=verifyUsernameKeyboard.get_markup())
                return
            bot.send_message(message.chat.id,
                             "لطفا نوع غذای خود را بفرستید - برای نمونه : قورمه سبزی کامل. برای انصراف /cancel ارسال نمایید.")
            database.Session.create_session(message.chat.id, UserSessionStates.WAITING_TO_SEND_FOOD_DESC)


class VerifyNotUserNameKeyboard(BaseInlineKeyboard):

    @handle_db
    def do_action(self, action: str, message):
        if action == "verify":
            bot.send_message(message.chat.id,
                             "لطفا نوع غذای خود را بفرستید - برای نمونه : قورمه سبزی کامل. برای انصراف /cancel ارسال نمایید.")
            database.Session.create_session(message.chat.id,
                                            UserSessionStates.WAITING_TO_SEND_FOOD_DESC_WITHOUT_USERNAME)
        else:
            bot.delete_message(message.chat.id, message.message_id)


class DontShowAlertsKeyboard(BaseInlineKeyboard):

    @handle_db
    def do_action(self, action: str, message):
        if action == "hideAlerts":
            user = database.User.get(chat_id=message.chat.id)
            database.UserCustomConfigs.get_or_create(user=user,
                                                     custom_config_mode=UserCustomConfigsEnum.DONT_SHOW_ALERTS.value)
            bot.send_message(message.chat.id,
                             "اطلاعیه ها از این به بعد نمایش داده نمی شوند. برای برگشت از /show_alerts استفاده کنید.")


admin_keyboard = AdminKeyboard([telebot.types.InlineKeyboardButton(text='آمار', callback_data=f'0status'),
                                telebot.types.InlineKeyboardButton(text='کاربران', callback_data=f'0getUsers'),
                                telebot.types.InlineKeyboardButton(text='ارسال اطلاعیه', callback_data=f'0alert'),
                                telebot.types.InlineKeyboardButton(text='اطلاعیه تست',
                                                                   callback_data=f'0alertTest')],
                               unique_id=0, row_width=4)

user_keyboard_hidden_words = UserKeyboardHiddenWords(
    [telebot.types.InlineKeyboardButton(text='نمایش عبارات فیلتر شده', callback_data=f'1view'),
     telebot.types.InlineKeyboardButton(text='اضافه کردن عبارت به فیلتر عدم نمایش', callback_data=f'1dontshow'),
     telebot.types.InlineKeyboardButton(text='حذف عبارت از فیلتر عدم نمایش', callback_data=f'1show'),
     telebot.types.InlineKeyboardButton(text='ریست کردن کلمات در فیلتر عدم نمایش', callback_data=f'1reset')],
    unique_id=1, row_width=4)

homeworkKeyboard = HomeworkKeyboard(
    [telebot.types.InlineKeyboardButton(text='انجام دادم', callback_data=f'2done')],
    unique_id=2, row_width=1
)

getFoodKeyboard = GetFoodKeyboard(
    [telebot.types.InlineKeyboardButton(text='دریافت غذا', callback_data=f'3getFood')],
    unique_id=3, row_width=1
)

foodKeyboard = FoodKeyboard(
    [telebot.types.InlineKeyboardButton(text='مشاهده لیست غذا های امروز', callback_data=f'4sendFoods'),
     telebot.types.InlineKeyboardButton(text='به اشتراک گذاشتن کد فراموشی', callback_data=f'4shareFood')],
    unique_id=4, row_width=1
)

verifyUsernameKeyboard = VerifyNotUserNameKeyboard(
    [telebot.types.InlineKeyboardButton(text='تایید می کنم', callback_data=f'5verify'),
     telebot.types.InlineKeyboardButton(text='تایید نمیکنم', callback_data=f'5notVerify')],
    unique_id=5, row_width=1
)

dontShowAlertsKeyboard = DontShowAlertsKeyboard(
    [telebot.types.InlineKeyboardButton(text='عدم نمایش اطلاعیه ها', callback_data=f'6hideAlerts')],
    unique_id=6, row_width=1
)


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call=None):
    inline_keyboards = {"0": admin_keyboard, "1": user_keyboard_hidden_words, "2": homeworkKeyboard,
                        "3": getFoodKeyboard, "4": foodKeyboard, "5": verifyUsernameKeyboard,
                        "6": dontShowAlertsKeyboard}
    current_keyboard = inline_keyboards[call.json['data'][0:1]]
    action = call.json['data'][1:]
    if action == "back" and current_keyboard.prev_markup is not None:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=current_keyboard.prev_markup)
    else:
        current_keyboard.do_action(action, call.message)
    bot.answer_callback_query(call.id)
