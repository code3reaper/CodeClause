import tkinter as tk
from tkinter import messagebox
import sqlite3
from main import open_main_window

def save_config():
    email = email_entry.get()
    smtp_server = smtp_server_entry.get()
    smtp_port = smtp_port_entry.get()
    smtp_user = smtp_user_entry.get()
    smtp_pass = smtp_pass_entry.get()
    
    conn = sqlite3.connect('email_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (email, smtp_server, smtp_port, smtp_user, smtp_pass) VALUES (?, ?, ?, ?, ?)",
              (email, smtp_server, smtp_port, smtp_user, smtp_pass))
    conn.commit()
    conn.close()
    config_window.destroy()
    open_main_window()

def open_config_window():
    global config_window, email_entry, smtp_server_entry, smtp_port_entry, smtp_user_entry, smtp_pass_entry
    config_window = tk.Tk()
    config_window.title("SMTP Configuration")

    tk.Label(config_window, text="Email").pack()
    email_entry = tk.Entry(config_window)
    email_entry.pack()

    tk.Label(config_window, text="SMTP Server").pack()
    smtp_server_entry = tk.Entry(config_window)
    smtp_server_entry.pack()

    tk.Label(config_window, text="SMTP Port").pack()
    smtp_port_entry = tk.Entry(config_window)
    smtp_port_entry.pack()

    tk.Label(config_window, text="SMTP User").pack()
    smtp_user_entry = tk.Entry(config_window)
    smtp_user_entry.pack()

    tk.Label(config_window, text="SMTP Password").pack()
    smtp_pass_entry = tk.Entry(config_window, show="*")
    smtp_pass_entry.pack()

    tk.Button(config_window, text="Save Configuration", command=save_config).pack()

    config_window.mainloop()
