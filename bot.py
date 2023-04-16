# importing necessary sections
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
            if user_session.waiting_action == AdminSessionStates.WAITING_TO_SEND_TEST_ALERT:
                send_alert_v2_test(message)

        Session.delete_instance(user_session)


bot.infinity_polling()
