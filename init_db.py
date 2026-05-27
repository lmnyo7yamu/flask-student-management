import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('database.db')
print("Database opened successfully!")

# Added 'age' column to the original tutorial code
conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, age TEXT, addr TEXT, city TEXT, pin TEXT)')
print("Table created successfully!")

conn.close()
