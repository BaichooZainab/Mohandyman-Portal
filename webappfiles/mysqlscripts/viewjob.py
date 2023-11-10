import mysql.connector
import dbconnect
cur, con = dbconnect.get_connection()

cur.execute("")
myresult = cur.fetchone()
for x in myresult:
    print(x)