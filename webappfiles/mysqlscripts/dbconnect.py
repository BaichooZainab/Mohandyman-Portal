import mysql.connector


def get_connection():
    con = mysql.connector.connect(
        host="localhost", user="root", password="", db="jobportaldb")
    cur = con.cursor()
    return cur, con
