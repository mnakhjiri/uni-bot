from database import *
from playhouse.migrate import *

migrator = MySQLMigrator(database)


def migrate():
    with database.atomic():
        migrate(
            migrator.add_column('user', 'is_ban', BooleanField(default=False))
        )
