import sqlite3

conn = sqlite3.connect('class.db')
print("Opened database successfully")

conn.execute('CREATE TABLE details (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print("Table created successfully")
conn.close()