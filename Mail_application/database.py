import sqlite3

def init_db():
    conn = sqlite3.connect('email_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, email TEXT, smtp_server TEXT, smtp_port INTEGER, smtp_user TEXT, smtp_pass TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sent_emails
                 (id INTEGER PRIMARY KEY, user_id INTEGER, to_email TEXT, subject TEXT, body TEXT, sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
