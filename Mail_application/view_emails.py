import tkinter as tk
import sqlite3

def view_sent_emails():
    conn = sqlite3.connect('email_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sent_emails")
    emails = c.fetchall()
    conn.close()

    sent_emails_window = tk.Tk()
    sent_emails_window.title("Sent Emails")

    for email in emails:
        email_label = tk.Label(sent_emails_window, text=f"To: {email[2]}, Subject: {email[3]}, Date: {email[5]}")
        email_label.pack()

    sent_emails_window.mainloop()
