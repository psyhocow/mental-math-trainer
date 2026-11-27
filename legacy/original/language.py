import tkinter as tk
import ttkbootstrap as ttk
import Shared
from Shared import Shared

class LanguageMessage:
    def __init__(self, parent, title, *options):
        self.parent = parent
        self.title = title
        self.options = options
        
        top = self.top = tk.Toplevel(parent)
        top.title(title)
        self.var = tk.StringVar(value='')  # Var to hold the choice
        top.geometry('270x150')
         
        for option in options:
            btn = ttk.Button(top, text=option, command=lambda opt=option: self.set_choice(opt))
            btn.pack(pady=5, padx=10, fill='x')

        Shared.register(self)

    def set_choice(self, choice):
        Shared.set_language(choice)  # Set the chosen language
        self.var.set(choice)  # Set the choice in the variable
        self.top.destroy()  # Close the popup window

        # Add a debug message to confirm that the language change event is triggered

        # After triggering the language change event, ensure that UI elements are updated
        Shared.notify_language_change()


    def update_texts(self):
        # Update text for all registered UI elements
        for child in self.parent.winfo_children():
            if isinstance(child, ttk.Label) or isinstance(child, ttk.Button):
                identifier = child.cget("text")
                translated_text = Shared.get_text(identifier)
                child.config(text=translated_text)
