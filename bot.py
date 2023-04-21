# importing necessary sections
import sections.user
from utils.enums import *
from sections.admin import *
from sections.user import *
from database import *

bot = settings.bot


@bot.message_handler()
@save_user_to_db
def handling_message(message):
    user_session = Session.get_or_none(user=User.get(chat_id=message.chat.id))
    if user_session is not None:
        if utils.is_admin(message.chat.id):
            if user_session.waiting_action == AdminSessionStates.WAITING_TO_SEND_ALERT:
                send_alert_v2(message)
            elif user_session.waiting_action == AdminSessionStates.WAITING_TO_SEND_TEST_ALERT:
                send_alert_v2_test(message)
        if user_session.waiting_action == UserSessionStates.WAITING_TO_SEND_SHOW_WORD:
            sections.user.show_word_v2(message)
        elif user_session.waiting_action == UserSessionStates.WAITING_TO_SEND_DONT_SHOW_WORD:
            sections.user.dont_show_word_v2(message)
        elif user_session.waiting_action == UserSessionStates.WAITING_TO_SEND_FOOD_DESC:
            FoodCode.add_food_code(message.chat.id, message.text)
            bot.send_message(message.chat.id, "با موفقیت اضافه شدید.")
        elif user_session.waiting_action == UserSessionStates.WAITING_TO_SEND_FOOD_DESC_WITHOUT_USERNAME:
            FoodCode.add_food_code(message.chat.id, message.text)
            bot.send_message(message.chat.id, "با موفقیت اضافه شدید.")

        Session.delete_instance(user_session)


bot.infinity_polling()
