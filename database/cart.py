import sqlite3

connection = sqlite3.connect('ShoppingCart.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS cart')
cursor.execute(
    '''CREATE TABLE cart(
        id INTEGER PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        product_id INTEGER NOT NULL UNIQUE,
        product_name TEXT NOT NULL,
        quantity INTEGER 
    )'''
)

connection.commit()
connection.close()

print("Cart table create successfully!")