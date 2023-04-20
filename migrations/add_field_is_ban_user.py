from playhouse.migrate import *

from ..database import *

migrator = MySQLMigrator(database)


def migrate():
    with database.atomic():
        migrate(
            migrator.add_column('user', 'is_ban', BooleanField(default=False))
        )
