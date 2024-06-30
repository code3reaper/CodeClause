import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3

import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import socket

def send_email():
    conn = sqlite3.connect('email_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    user = c.fetchone()
    conn.close()

    from_email = user[1]
    smtp_server = user[2]
    smtp_port = user[3]
    smtp_user = user[4]
    smtp_pass = user[5]

    to_email = to_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        conn = sqlite3.connect('email_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO sent_emails (user_id, to_email, subject, body) VALUES (?, ?, ?, ?)",
                  (user[0], to_email, subject, body))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        messagebox.showerror("Authentication Error", f"Failed to authenticate. Check the SMTP user and password.\n{str(e)}")
    except smtplib.SMTPConnectError as e:
        messagebox.showerror("Connection Error", f"Failed to connect to the server. Check the SMTP server and port.\n{str(e)}")
    except smtplib.SMTPRecipientsRefused as e:
        messagebox.showerror("Recipient Error", f"The recipient address was refused by the server.\n{str(e)}")
    except socket.gaierror as e:
        messagebox.showerror("Network Error", f"Network error occurred. Ensure the SMTP server address is correct and you have an internet connection.\n{str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def open_main_window():
    global main_window, to_entry, subject_entry, body_text
    main_window = tk.Tk()
    main_window.title("Send Email")

    tk.Label(main_window, text="To").pack()
    to_entry = tk.Entry(main_window)
    to_entry.pack()

    tk.Label(main_window, text="Subject").pack()
    subject_entry = tk.Entry(main_window)
    subject_entry.pack()

    tk.Label(main_window, text="Body").pack()
    body_text = tk.Text(main_window, height=10, width=50)
    body_text.pack()

    tk.Button(main_window, text="Send Email", command=send_email).pack()

    main_window.mainloop()
    conn = sqlite3.connect('email_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    user = c.fetchone()
    conn.close()

    from_email = user[1]
    smtp_server = user[2]
    smtp_port = user[3]
    smtp_user = user[4]
    smtp_pass = user[5]

    to_email = to_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        conn = sqlite3.connect('email_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO sent_emails (user_id, to_email, subject, body) VALUES (?, ?, ?, ?)",
                  (user[0], to_email, subject, body))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_main_window():
    global main_window, to_entry, subject_entry, body_text
    main_window = tk.Tk()
    main_window.title("Send Email")

    tk.Label(main_window, text="To").pack()
    to_entry = tk.Entry(main_window)
    to_entry.pack()

    tk.Label(main_window, text="Subject").pack()
    subject_entry = tk.Entry(main_window)
    subject_entry.pack()

    tk.Label(main_window, text="Body").pack()
    body_text = tk.Text(main_window, height=10, width=50)
    body_text.pack()

    tk.Button(main_window, text="Send Email", command=send_email).pack()

    main_window.mainloop()
