# setup_db.py
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('url_shortener.db')
c = conn.cursor()

# Create a table to store URLs
c.execute('''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY,
    long_url TEXT NOT NULL,
    short_url TEXT NOT NULL
)
''')
conn.commit()
conn.close()
