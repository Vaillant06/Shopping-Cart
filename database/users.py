import sqlite3

connection = sqlite3.connect('ShoppingCart.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS cartUsers')
cursor.execute(
    '''CREATE TABLE cartUsers(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        phone_number INTEGER(10) NOT NULL UNIQUE
    )'''
)

connection.commit()
connection.close()

print("Users table create successfully!")