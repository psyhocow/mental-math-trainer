import Shared, tkinter as tk, ttkbootstrap as ttk, random
from Menu import StartPage
from datetime import datetime, timedelta
from sound import play_sound

class TrainerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.score = StartPage.return_score(self.score, self.score)
        
        TrainerPage.current_difficulty = 'normal'
        self.start_page = self.controller.frames[StartPage]
        self.timer_bar = tk.Canvas(self, height=20, bg='green')
        self.timer_bar.pack(fill=tk.X, side=tk.TOP)
        self.timer_fill = self.timer_bar.create_rectangle(0, 0, self.timer_bar.winfo_reqwidth(), 20, fill='green', tags='timer_fill')
        self.right_answers = 0
        self.wrong_answers = 0
        self.question_label = ttk.Label(self, font=Shared.fnt)
        self.question_label.pack(pady=20)
        self.answer_entry = ttk.Entry(self, font=Shared.fnt)
        self.answer_entry.pack(pady=20)
        self.answer_entry.bind('<Return>', self.submit_answer)

        submit_button = ttk.Button(self, text="Submit", command=self.submit_answer).pack(pady=20)
        self.right_answer_label = ttk.Label(self, text=f"{Shared.get_text('right')}{self.right_answers}", font='Verdana 14')
        self.right_answer_label.place(relx=0.01, rely=0.9, anchor='sw')
        self.wrong_answer_label = ttk.Label(self, text=f"{Shared.get_text('wrong')}{self.wrong_answers}", font='Verdana 14')
        self.wrong_answer_label.place(relx=0.01, rely=0.99, anchor='sw')
        self.generate_new_question()
        
    def submit_answer(self, event=None):
        user_answer = self.answer_entry.get()
        if user_answer != "":
            if hasattr(self, 'correct_answer'):
                correct_answer = self.correct_answer
                try:
                    user_answer = int(user_answer)
                    if user_answer == correct_answer:
                        print("Correct")
                        play_sound('right')
                        self.right_answers += 1
                    else:
                        print("Wrong")
                        play_sound('wrong')
                        self.wrong_answers += 1
                    self.update_answers_labels()
                    self.generate_new_question()
                except ValueError:
                    print("Error: Please enter a valid integer.")
            else:
                print("Error: Please generate a new question first.")
        else:
            print("Error: Please enter an answer.")

    def generate_new_question(self):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        operation = random.choice(["+", "-"])

        if operation == "+":
            correct_answer = a + b
        else:
            correct_answer = a - b

        if correct_answer < 0:
            print("Skipping question: answer is not natural and not 0")
            return self.generate_new_question()

        question = f"{a} {operation} {b} = ?"
        print("Generated Question:", question, correct_answer)
        self.correct_answer = correct_answer
        self.question_label.config(text=question)
        self.answer_entry.delete(0, 'end')

    def initialize_timer(self):
        if self.current_difficulty == 'easy': timer_length = 20
        elif self.current_difficulty == 'normal': timer_length = 15
        elif self.current_difficulty == 'hard': timer_length = 10
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=timer_length)
        self.right_answers = 0
        self.wrong_answers = 0
        self.right_answer_label.config(text=f"{Shared.get_text('right')}{self.right_answers}")
        self.wrong_answer_label.config(text=f"{Shared.get_text('wrong')}{self.right_answers}")
        self.update_timer_bar()
        

    def update_timer_bar(self):
        if self.current_difficulty == 'easy': timer_length = 20
        elif self.current_difficulty == 'normal': timer_length = 15
        elif self.current_difficulty == 'hard': timer_length = 10
        now = datetime.now()
        remaining_seconds = (self.end_time - now).total_seconds()
        self.controller.title(f"{Shared.nme} - {Shared.get_text('time_remaining')}{timedelta(seconds=round(remaining_seconds))}")
        total_width = self.timer_bar.winfo_width()
        new_width = max(0, total_width * (remaining_seconds / timer_length))
        self.timer_bar.delete(self.timer_fill)
        self.timer_fill = self.timer_bar.create_rectangle(0, 0, new_width, 20, fill='green', tags='timer_fill')
        percentage = remaining_seconds / timer_length
        color = 'red' if percentage < 1/3 else 'orange' if percentage < 2/3 else 'green'
        self.timer_bar.itemconfig(self.timer_fill, fill=color)
        if remaining_seconds > 0:
            self.after(1000, self.update_timer_bar)
        else:
            self.on_timer_end()

    def on_timer_end(self):
        print("Time's up!")
        self.controller.title(Shared.nme)
        self.controller.show_frame(StartPage)
        score = self.right_answers
        self.controller.frames[StartPage].scoreWriteToFile(score)
        self.answer_entry.delete(0, 'end')    
        self.start_page.update_best_score_label(self.start_page.scoreReadFromFile())

    def update_answers_labels(self):
        self.right_answer_label.config(text=f"{Shared.get_text('right')}{self.right_answers}")
        self.wrong_answer_label.config(text=f"{Shared.get_text('wrong')}{self.wrong_answers}")
    
from Shared import Shared
from Difficulty import DifficultyMessage

