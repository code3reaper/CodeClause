# app.py
import tkinter as tk
from tkinter import messagebox
import webbrowser
from url_shortener import save_url

class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener")
        self.root.geometry("500x300")  # Set window size
        self.root.configure(bg='#f0f0f0')  # Set background color

        # Create main frame
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(expand=True, fill='both')

        self.title_label = tk.Label(self.main_frame, text="URL Shortener", font=("Arial", 20, "bold"), bg='#f0f0f0')
        self.title_label.pack(pady=(20, 10))

        self.label = tk.Label(self.main_frame, text="Enter the long URL:", font=("Arial", 12), bg='#f0f0f0')
        self.label.pack()

        self.url_entry = tk.Entry(self.main_frame, width=50, font=("Arial", 10))
        self.url_entry.pack(pady=5)

        self.shorten_button = tk.Button(self.main_frame, text="Shorten", font=("Arial", 12, "bold"), bg='#4CAF50', fg='white',
                                        command=self.shorten_url)
        self.shorten_button.pack(pady=10)

        self.short_url_label = tk.Label(self.main_frame, text="", font=("Arial", 12), fg="blue", cursor="hand2", bg='#f0f0f0')
        self.short_url_label.pack(pady=10)
        self.short_url_label.bind("<Button-1>", self.open_url)

        self.short_url = None

    def shorten_url(self):
        long_url = self.url_entry.get()
        if long_url:
            short_url = save_url(long_url)
            self.short_url = f"http://127.0.0.1:5000/{short_url}"
            self.short_url_label.config(text=f"Short URL: {self.short_url}")
            self.url_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid URL.")

    def open_url(self, event):
        if self.short_url:
            webbrowser.open(self.short_url)

if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()
