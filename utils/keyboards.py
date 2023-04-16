import telebot
import settings

bot = settings.bot


class BaseInlineKeyboard:
    # keyboard_buttons = [telebot.types.InlineKeyboardButton(text='❌', callback_data=f'dislikeP'),
    #                     telebot.types.InlineKeyboardButton(text='📃', callback_data=f'lyrics')]

    def __init__(self, keyboard_buttons, unique_id=0, row_width=1, prev_markup=None):
        self.keyboard_buttons = keyboard_buttons
        self.unique_id = unique_id
        self.row_width = row_width
        self.prev_markup = prev_markup

    @bot.callback_query_handler(func=lambda call: True)
    def back_button(self, call):
        if call.json['data'] == f"back{self.prev_markup}":
            if self.prev_markup is not None:
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, self.prev_markup)

    def get_markup(self):
        return telebot.types.InlineKeyboardMarkup([self.keyboard_buttons], row_width=self.row_width)


test = BaseInlineKeyboard([telebot.types.InlineKeyboardButton(text='❌', callback_data=f'test')], unique_id=1)
