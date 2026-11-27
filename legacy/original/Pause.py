import tkinter as tk, ttkbootstrap as ttk

class PauseMessage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        
        top = self.top = tk.Toplevel(parent)
        top.title('Pause')
        top.geometry('210x80')

        btn_continue = ttk.Button(top, text='Continue')
        btn_continue.pack(pady=5, padx=10, fill='both')

        btn_cancel = ttk.Button(top, text="Cancel to menu")
        btn_cancel.pack(pady=5, padx=10, fill='both')

from Menu import StartPage
