import tkinter as tk, ttkbootstrap as ttk

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text = 'Settings Menu', font = Shared.fnt)
        label.pack()
        
        button1 = ttk.Button(self, text = 'Menu',
            command = lambda : controller.show_frame(StartPage)).pack(
            padx = 10, pady = 15)     

from Menu import StartPage
from Shared import Shared
