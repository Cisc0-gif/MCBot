import sqlite3

username = input("Enter discord username (name#1234): ")

conn = sqlite3.connect("Members.db")
crsr = conn.cursor()

crsr.execute("UPDATE users SET perms == '1' WHERE name == '" + username + "'")
conn.commit()
conn.close()
