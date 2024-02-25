import tkinter as tk
from playsound import playsound
import os

class CopeTimer:
    def __init__(self, window):
        self.window = window
        window.title("CopeTimer")
        
        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)
        self.worktime = 3600 # 1 hour time fixed
        self.breaktime1 = 300 # 5 minute break
        # Elements:
        
        self.label = tk.Label(window, text="KEEP WORKING!!!",font=("Georgia",20))
        button1 = tk.Button(window, text="RESET", command=self.reset_timer,width = 5, height = 1,font='Georgia',relief='ridge')

        self.timer_label = tk.Label(window, text="",font=("Georgia",40))


        # Pack elements:

        self.label.pack(padx=10, pady=10)
        self.timer_label.pack(pady=10)
        button1.pack()
        #self.remaining_time = 3600  # 1 hour
        self.remaining_time = self.worktime

        # call update timer
        window.after(1000, self.update_timer)

    def update_timer(self):
        # Update the timer label
        minutes, seconds = divmod(self.remaining_time, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        #self.timer_label.config(text=f"Time remaining: {time_str}")
        self.timer_label.config(text=f"{time_str}")

        # timer end!
        if seconds == 0 and minutes == 0:
            self.play_ringtone()
        # Decrement the remaining time while not reached 0
        if self.remaining_time >= 1:
            self.remaining_time -= 1

        self.window.after(1000, self.update_timer)
    '''
    This function resets the timer to the specified worktime
    '''
    def play_ringtone(self):
        playsound(os.path.join(os.path.dirname(__file__), 'sounds', 'ring.wav'))
    def reset_timer(self):
        self.remaining_time = self.worktime

    def close_window(self):
        # Function to close the window
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    window = tk.Tk()
    app = CopeTimer(window)
    app.run()
