import mysql.connector
import dbconnect

cur, con = dbconnect.get_connection()
cur.execute("SHOW TABLES")

for x in cur:
    print(x)
