import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port=3307,
    database="userdata"
)
mycursor=mydb.cursor()
mycursor.execute('select * from users')
users=mycursor.fetchall()

for user in users:
    print(user)