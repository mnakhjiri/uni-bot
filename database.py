from peewee import *
from datetime import datetime

# peewee.Context conflicts with the context.Context

database = SqliteDatabase("db.sqlite3")


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
        return list(query)

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


def create_tables():
    with database:
        database.create_tables([User, BlackListWord])


create_tables()
