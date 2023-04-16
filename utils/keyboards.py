import telebot
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
        if self.prev_markup is not None:
            keyboards = self.keyboard_buttons
            keyboards.append(telebot.types.InlineKeyboardButton(text='برگشت', callback_data=f'{self.unique_id}back'))
            return telebot.types.InlineKeyboardMarkup([keyboards], row_width=self.row_width)
        else:
            return telebot.types.InlineKeyboardMarkup([self.keyboard_buttons], row_width=self.row_width)

    def do_action(self, action: str, message):
        pass


class AdminKeyboard(BaseInlineKeyboard):
    def do_action(self, action: str, message):
        if action == "status":
            print("status")
            admin.status(message)
        elif action == "getUsers":
            admin.get_users(message)


admin_keyboard = BaseInlineKeyboard([telebot.types.InlineKeyboardButton(text='آمار', callback_data=f'0status'),
                                     telebot.types.InlineKeyboardButton(text='کاربران', callback_data=f'0getUsers')],
                                    unique_id=0)


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
