import tkinter as tk
from tkinter import messagebox
from config import open_config_window

def login():
    email = email_entry.get()
    password = password_entry.get()
    if email and password:
        root.destroy()  # Close the login window
        open_config_window()  # Open the configuration window
    else:
        messagebox.showerror("Error", "Please enter both email and password.")

root = tk.Tk()
root.title("Email Application Login")

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login).pack()

root.mainloop()
