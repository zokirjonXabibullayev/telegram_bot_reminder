import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
telegram_id INTEGER,
name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
text TEXT,
file_id TEXT,
file_type TEXT,
category_id INTEGER,
date TEXT,
done INTEGER DEFAULT 0
)
""")

conn.commit()
