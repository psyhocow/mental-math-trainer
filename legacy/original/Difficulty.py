import tkinter as tk, ttkbootstrap as ttk
from Shared import Shared 


class DifficultyMessage:
    def __init__(self, parent, title_key, callback, *option_keys):
        self.parent = parent
        self.title_key = title_key
        self.option_keys = option_keys
        self.callback = callback
        
        self.top = tk.Toplevel(parent)
        self.top.title(Shared.get_text(title_key))  # Use Shared module for initial title text
        self.var = tk.StringVar(value='')  # Var to hold the choice
        self.top.geometry('270x150')
        
        self.buttons = []  # Keep track of buttons for later updates
        
        for option_key in option_keys:
            btn = ttk.Button(self.top, text=Shared.get_text(option_key), command=lambda opt=option_key: self.set_choice(opt))
            btn.pack(pady=5, padx=10, fill='x')
            self.buttons.append((btn, option_key))  # Store button and its text key
        
        # Register this dialog to receive language change notifications
        Shared.register(self)

    def set_choice(self, choice):
        self.var.set(choice)  # Set the choice
        self.callback(choice)
        self.top.destroy()
    
    def update_texts(self):
        # Update the title and button texts based on the current language
        if self.top.winfo_exists():
            self.top.title(Shared.get_text(self.title_key))
            for btn, key in self.buttons:
                btn.config(text=Shared.get_text(key))
        else: pass