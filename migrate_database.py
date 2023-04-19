import database_temp
import database

for sqlite_record in database_temp.database.select():
    database.database.create(name=sqlite_record.name, age=sqlite_record.age)
