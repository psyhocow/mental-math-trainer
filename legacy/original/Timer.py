import Shared
from Menu import StartPage
from datetime import datetime, timedelta


def initialize_timer(self):
    self.start_time = datetime.now()
    self.end_time = self.start_time + timedelta(seconds=self.timer_length)
    self.update_timer_bar()
        
def update_timer_bar(self):
    now = datetime.now()
    remaining_seconds = (self.end_time - now).total_seconds()
    # if remaining_seconds <= 0:
    #     remaining_seconds = 0        #     self.controller.title("Name")
    self.controller.title(f"Time Remaining: {timedelta(seconds=round(remaining_seconds))}")

    # Calculate the new width of the timer fill based on remaining time
    total_width = self.timer_bar.winfo_width()
    new_width = max(0, total_width * (remaining_seconds / self.timer_length))

        # Clear the existing timer fill rectangle
    self.timer_bar.delete(self.timer_fill)

        # Create the new timer fill rectangle with the updated width
    self.timer_fill = self.timer_bar.create_rectangle(0, 0, new_width, 20, fill='green', tags='timer_fill')

        # Update the fill color based on time remaining
    percentage = remaining_seconds / self.timer_length
    color = 'red' if percentage < 1/3 else 'orange' if percentage < 2/3 else 'green'
    self.timer_bar.itemconfig(self.timer_fill, fill=color)

    if remaining_seconds > 0:
        self.after(1000, self.update_timer_bar)
    else:
        self.on_timer_end(self.controller)
            

def on_timer_end(self, controller):
    print("Time's up!")
    self.remaining_seconds = 0
    self.controller.title(Shared.nme)
    self.controller.show_frame(StartPage)
    self.answer_entry.delete(0, 'end')