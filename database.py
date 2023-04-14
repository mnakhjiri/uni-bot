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


def create_tables():
    with database:
        database.create_tables([User])


create_tables()
