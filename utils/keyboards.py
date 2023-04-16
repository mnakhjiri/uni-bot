import telebot
from utils.enums import AdminSessionStates
import database
import settings
from sections import admin

bot = settings.bot


class BaseInlineKeyboard:
    def __init__(self, keyboard_buttons, unique_id=0, row_width=1, prev_markup=None):
        self.keyboard_buttons = keyboard_buttons
        self.unique_id = unique_id
        self.row_width = row_width
        self.prev_markup = prev_markup

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
    def do_action(self, action: str, message):
        if action == "status":
            print("status")
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


admin_keyboard = AdminKeyboard([telebot.types.InlineKeyboardButton(text='آمار', callback_data=f'0status'),
                                telebot.types.InlineKeyboardButton(text='کاربران', callback_data=f'0getUsers'),
                                telebot.types.InlineKeyboardButton(text='ارسال اطلاعیه', callback_data=f'0alert'),
                                telebot.types.InlineKeyboardButton(text='اطلاعیه تست',
                                                                   callback_data=f'0alertTest')],
                               unique_id=0, row_width=4)


# test2 = BaseInlineKeyboard([telebot.types.InlineKeyboardButton(text='❌', callback_data=f'test')], unique_id=1,
#                            prev_markup=test.get_markup())


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call=None):
    inline_keyboards = {"0": admin_keyboard}
    current_keyboard = inline_keyboards[call.json['data'][0:1]]
    action = call.json['data'][1:]
    if action == "back" and current_keyboard.prev_markup is not None:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=current_keyboard.prev_markup)
    else:
        current_keyboard.do_action(action, call.message)
    bot.answer_callback_query(call.id)
