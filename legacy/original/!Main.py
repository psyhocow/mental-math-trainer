import tkinter as tk, ttkbootstrap as ttk

from Menu import StartPage
from Trainer import TrainerPage
from Shared import nme, fnt, paused, set_paused
from Settings import SettingsPage

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs): # init MainApp
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('560x315')
        self.resizable(False, False)
        self.title(nme)
        
        container = ttk.Frame(self)  
        container.pack()#side = 'top', fil = 'both', expand = True
        container.grid_columnconfigure(0, weight = 1)
        container.grid_rowconfigure(0, weight = 1)
        
        self.frames = {} # creating of pages.
        self.current_page = None
        
        for f in (StartPage, TrainerPage, SettingsPage):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = 'NWSE')
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.current_page = frame
# start an app
app = MainApp()
app.mainloop()