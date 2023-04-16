import telebot
import settings

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


test = BaseInlineKeyboard([telebot.types.InlineKeyboardButton(text='❌', callback_data=f'test')], unique_id=0)
test2 = BaseInlineKeyboard([telebot.types.InlineKeyboardButton(text='❌', callback_data=f'test')], unique_id=1,
                           prev_markup=test.get_markup())


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call=None):
    inline_keyboards = {"0": test, "1": test2}
    current_keyboard = inline_keyboards[call.json['data'][0:1]]
    if current_keyboard.prev_markup is not None:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=current_keyboard.prev_markup)