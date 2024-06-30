import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(0, 0)

        self.expression = ""
        self.result_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Display frame
        display_frame = ttk.Frame(self.root)
        display_frame.pack(expand=True, fill="both")

        # Result display
        result_display = ttk.Entry(
            display_frame, textvariable=self.result_var, font=("Helvetica", 24), justify='right')
        result_display.pack(expand=True, fill="both")

        # Button frame
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(expand=True, fill="both")

        # Buttons layout
        buttons = [
            '7', '8', '9', '/', 
            '4', '5', '6', '*', 
            '1', '2', '3', '-', 
            '0', '.', '=', '+'
        ]

        # Creating buttons and placing them in the grid
        row_val = 0
        col_val = 0
        for button in buttons:
            if button == '=':
                ttk.Button(buttons_frame, text=button, command=self.evaluate_expression).grid(row=row_val, column=col_val, sticky='nsew')
            else:
                ttk.Button(buttons_frame, text=button, command=lambda b=button: self.update_expression(b)).grid(row=row_val, column=col_val, sticky='nsew')

            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # Adding row and column configurations
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)

    def update_expression(self, value):
        self.expression += str(value)
        self.result_var.set(self.expression)

    def evaluate_expression(self):
        try:
            result = str(eval(self.expression))
            self.result_var.set(result)
            self.expression = result
        except Exception as e:
            self.result_var.set("Error")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
