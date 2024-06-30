# url_shortener.py
import sqlite3
import string
import random

# Connect to the SQLite database
conn = sqlite3.connect('url_shortener.db', check_same_thread=False)
c = conn.cursor()

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(length))
    return short_url

def save_url(long_url):
    short_url = generate_short_url()
    
    # Check for uniqueness of the short URL
    while c.execute('SELECT short_url FROM urls WHERE short_url = ?', (short_url,)).fetchone():
        short_url = generate_short_url()

    c.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
    conn.commit()
    
    return short_url

def get_long_url(short_url):
    c.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,))
    result = c.fetchone()
    if result:
        return result[0]
    return None
