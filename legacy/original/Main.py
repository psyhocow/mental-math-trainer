import tkinter as tk, ttkbootstrap as ttk

from Menu import StartPage
from Trainer import TrainerPage
from Shared import Shared
from Pause import PauseMessage

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('560x315')
        self.resizable(False, False)
        self.title(Shared.nme)

        container = ttk.Frame(self)
        container.pack()
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        self.frames = {}
        self.current_page = None

        for frame_type in (StartPage, TrainerPage):
            frame = frame_type(container, self)
            self.frames[frame_type] = frame
            frame.grid(row=0, column=0, sticky='NWSE')
        self.show_frame(StartPage)

    def show_frame(self, frame_type):
        frame = self.frames[frame_type]
        frame.tkraise()
        self.current_page = frame
        if frame_type == TrainerPage:
            frame.initialize_timer()

app = MainApp()
app.mainloop()
