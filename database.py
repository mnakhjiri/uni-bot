from peewee import *
from datetime import datetime
import settings

mysql_database = None
if settings.mysql_active:
    mysql_database = MySQLDatabase(user=settings.db_user,
                                   password=settings.db_pass,
                                   host=settings.db_host,
                                   port=int(settings.db_port),
                                   database=settings.db_name, )

database = SqliteDatabase("db.sqlite3")
if mysql_database is not None:
    database = mysql_database


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    name = TextField()
    last_name = TextField()
    chat_id = TextField()

    @classmethod
    def add_user(cls, name, last_name, chat_id):
        # Temporary:
        if cls.have_user(chat_id):
            cls.update(name=name, last_name=last_name)
            return

        return cls.create(
            name=name,
            last_name=last_name,
            chat_id=chat_id
        )

    @classmethod
    def get_users(cls):
        query = User.select().execute()
        return list(query)

    @classmethod
    def have_user(cls, chat_id):
        query = cls.select().where((cls.chat_id == chat_id))
        return len(query) != 0


class BlackListWord(BaseModel):
    user = ForeignKeyField(User)
    text = TextField()

    @classmethod
    def get_black_list_words(cls, chat_id):
        user = User.get(chat_id=chat_id)
        query = cls.select().where((cls.user == user))
        items = list(query)
        result = []
        for item in items:
            result.append(item.text)
        return list(result)

    @classmethod
    def add_to_black_list(cls, word, chat_id):
        if word not in BlackListWord.get_black_list_words(chat_id):
            user = User.get(chat_id=chat_id)
            cls.create(
                user=user,
                text=word
            )

    @classmethod
    def remove_from_black_list(cls, word, chat_id):
        if word in BlackListWord.get_black_list_words(chat_id):
            user = User.get(chat_id=chat_id)
            record = cls.get(user=user, text=word)
            BlackListWord.delete_instance(record)

    @classmethod
    def remove_all_black_list(cls, chat_id):
        user = User.get(chat_id=chat_id)
        BlackListWord.delete().where(BlackListWord.user == user).execute()


# not a very nice way to handle user sessions, should fix it later
class Session(BaseModel):
    user = ForeignKeyField(User)
    waiting_action = TextField()
    json_saved_data = TextField(null=True)
    test = TextField(null=True)
    test2 = TextField(null=True)

    @classmethod
    def create_session(cls, chat_id: str, waiting_action: str, json_saved_data=None):
        user = User.get(chat_id=chat_id)
        prev_session = Session.get_or_none(user=user)
        if prev_session is not None:
            Session.delete_instance(prev_session)
        Session.create(user=user, waiting_action=waiting_action, json_saved_data=json_saved_data)


def create_tables():
    with database:
        database.create_tables([User, BlackListWord, Session])


create_tables()
