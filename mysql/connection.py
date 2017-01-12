from __future__ import print_function

import MySQLdb as my

db = my.connect(host="localhost", user="root", passwd="0807", db="test")
print(db)
cursor = db.cursor()
print(cursor)
data = cursor.execute("select * from test")
result = cursor.fetchall()

# cursor.execute("insert into test (email,pwd) values('test@gmail.com','test')")
# creat_table = "create table IF NOT EXISTS test (email varchar(70),pwd varchar(20));"
# cursor.execute(creat_table)
# db.commit()
# data = cursor.execute("select * from test")
print(result)
print(data)
