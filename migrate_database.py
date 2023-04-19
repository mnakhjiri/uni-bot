from playhouse.reflection import Introspector

from database import *

introspector = Introspector.from_database(database)
models = introspector.generate_models()
mysql_database.create_tables(list(models.values()))
mysql_database.close()
