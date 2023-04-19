import database_temp
import database

for user_record in database_temp.User.select():
    database.User.add_user(user_record.name, user_record.last_name, user_record.chat_id)

for record in database_temp.BlackListWord.select():
    database.BlackListWord.add_to_black_list(record.text, record.user.chat_id)
