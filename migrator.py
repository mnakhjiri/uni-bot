from playhouse.migrate import *
from database import *

migrator = MySQLMigrator(database)


def add_field_is_ban_user():
    with database.atomic():
        migrate(
            migrator.add_column('user', 'is_ban', BooleanField(default=False))
        )


add_field_is_ban_user()
