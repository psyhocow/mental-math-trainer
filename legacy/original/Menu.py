import tkinter as tk
import ttkbootstrap as ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        def popup_difficulty(controller):
            # Calls the popup dialog
            DifficultyMessage(self, 'Choose the difficulty:', self.handle_difficulty_choice, 'easy', 'normal', 'hard')
        
        def language_popup(controller):
            LanguageMessage(self, 'Choose the language', 'Kazakh', 'Russian', 'English')
              
        labelsFrame = tk.Frame(self, width=300, height=315)
        
        scoreFrame = tk.Frame(labelsFrame)
        self.label = ttk.Label(labelsFrame, text=Shared.nme, font=Shared.fnt)
        self.label.pack()
        
        self.score = tk.IntVar(value=0)
        self.score.set(self.scoreReadFromFile())
        
        self.scLabel2 = ttk.Label(scoreFrame, text=f'{Shared.get_text("best_score")}{self.score.get()}', font='Verdana 18')
        self.scLabel2.pack(side='left')
        
        
        
        scoreFrame.pack()
        
        labelsFrame.pack(side='left', pady=(40, 0))
        
        buttonsFrame = tk.Frame(self, width=196, height=315)
        
        self.button1 = ttk.Button(buttonsFrame, text=Shared.get_text("start"), width=30, command=lambda: [controller.show_frame(TrainerPage)])
        self.button1.pack(padx=10)

        self.button3 = ttk.Button(buttonsFrame, width=30, text=Shared.get_text("choose_difficulty"), command=lambda: popup_difficulty(controller))
        self.button3.pack(padx=10, pady=15)
    
        self.button4 = ttk.Button(buttonsFrame, width=30, text=Shared.get_text("language"), command=lambda: language_popup(controller))
        self.button4.pack(padx=10, pady=(0, 15))
        buttonsFrame.pack(side='right', pady=(40, 0))

        Shared.register(self)

        # Update UI elements with initial language
        self.update_texts()

    def update_texts(self):
        # Access TrainerPage instance directly
        if TrainerPage in self.controller.frames:
            trainer_page = self.controller.frames[TrainerPage]
            trainer_page.right_answer_label.config(text=Shared.get_text("right") + str(trainer_page.right_answers))
            trainer_page.wrong_answer_label.config(text=Shared.get_text("wrong") + str(trainer_page.wrong_answers))
        if StartPage in self.controller.frames:
            self.scLabel2.config(text=f'{Shared.get_text("best_score")}{self.score.get()}')
            self.button1.config(text=Shared.get_text("start"))
            self.button3.config(text=Shared.get_text("choose_difficulty"))
            self.button4.config(text=Shared.get_text("language"))
        
            
        # Update other UI elements similarly...


    def scoreWriteToFile(self, score):
        try:
            with open('Score.txt', 'r') as scoreFile:
                best_score = int(scoreFile.read())
                
        except FileNotFoundError:
            best_score = 0
        if score > best_score:
            print('Writing score:', score)  # Add this print statement
            with open('Score.txt', 'w') as scoreFile:
                scoreFile.write(str(score))
            self.score.set(best_score)
        self.scLabel2.config(text=f'{Shared.get_text("best_score")}{best_score}')
        
    def scoreReadFromFile(self):
        try:
            with open('Score.txt', 'r') as scoreFile:
                best_score = int(scoreFile.read())
            print('Reading score:', best_score)  # Add this print statement
            self.return_score(best_score)
            return best_score
        except FileNotFoundError:
            return 0
    
    def update_best_score_label(self, best_score):
        self.scLabel2.config(text=f'{Shared.get_text("best_score")}{best_score}')

    def handle_difficulty_choice(self, choice):
        # This method will be called with the chosen difficulty
        TrainerPage.current_difficulty = choice
    def return_score(self, score):
        TrainerPage.score = score
            
import Shared
from Shared import Shared
from Difficulty import DifficultyMessage
from language import LanguageMessage
from Trainer import TrainerPage


