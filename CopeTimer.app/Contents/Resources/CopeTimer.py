import tkinter as tk
from playsound import playsound
import os

class CopeTimerMenu:
    def __init__(self, window,copetimer):
        self.window = window
        self.time1=0
        self.time2=0
        self.copetimer = copetimer
        window.title("Menu")

        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)

        # Elements:
        
        self.label = tk.Label(window, text="MENU",font=("Georgia",15))
        self.label2 = tk.Label(window, text="work duration (seconds):",font=("Georgia",15))
        self.label3 = tk.Label(window, text="break duration (seconds):",font=("Georgia",15))
        button = tk.Button(window, text="DONE", command=self.set_values,width = 5, height = 1,font='Georgia',relief='ridge')

        self.entry1= tk.Entry(window, width= 10)
        self.entry2= tk.Entry(window, width= 10)
        self.entry1.focus_set()
        self.entry1.focus_set()
        

        # grid elements:

        self.label.grid(row = 0, column = 0, pady = 2)
        self.label2.grid(row = 1, column = 0, pady = 2)
        self.label3.grid(row = 2, column = 0, pady = 2)
        self.entry1.grid(row = 1, column = 1, pady = 2)
        self.entry2.grid(row = 2, column = 1, pady = 2)
        button.grid(row = 3, column = 1, pady = 2)


    def set_values(self):
        self.time1 = self.entry1.get()
        self.time2 = self.entry2.get()
        #print(self.time1)
        #print(self.time2)
        if self.time1.isnumeric() and self.time2.isnumeric():
            self.copetimer.set_worktime(int(self.time1))  
            self.copetimer.set_breaktime(int(self.time2))       
            self.close_window()
    def close_window(self):
        # Function to close the window
        self.window.destroy()

    def run(self):
        self.window.mainloop()

class CopeTimer:
    def __init__(self, window):
        self.window = window
        window.title("CopeTimer")
        self.phase = 0
        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)
        self.worktime = 3600 # 1 hour time fixed
        self.breaktime = 300 # 5 minute break
        # Elements:
        
        self.label = tk.Label(window, text="KEEP WORKING!!!",font=("Georgia",20))
        button1 = tk.Button(window, text="RESET", command=self.reset_timer,width = 5, height = 1,font='Georgia',relief='ridge')
        button2 = tk.Button(window, text="MENU", command=self.open_menu,width = 5, height = 1,font='Georgia',relief='ridge')

        self.timer_label = tk.Label(window, text="",font=("Georgia",40))


        # Pack elements:

        self.label.pack(padx=10, pady=10)
        self.timer_label.pack(pady=10)
        button1.pack(side="left")
        button2.pack(side="right")
        #self.remaining_time = 3600  # 1 hour
        self.remaining_time = self.worktime

        # call update timer
        window.after(1000, self.update_timer)

    def update_timer(self):
        # Update the timer label
        hours, remainder = divmod(self.remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=f"{time_str}")

        # Decrement the remaining time while not reached 0
        if self.remaining_time >= 1:
            self.remaining_time -= 1
            
        # timer end!
        if time_str == "00:00:00" and self.phase == 0:
            self.label.config(text="BREAK TIME!!!", fg='dark green')
            self.window.after(1000, self.play_ringtone)
        if time_str == "00:00:00" and self.phase == 1:
            self.label.config(text="KEEP WORKING!!!", fg='black')
            self.window.after(1000, self.play_ringtone)
        self.window.after(1000, self.update_timer)

    def set_worktime(self,time):
        self.worktime = time
    def set_breaktime(self,time):
        self.breaktime = time
    def play_ringtone(self):
        playsound(os.path.join(os.path.dirname(__file__), 'sounds', 'ring.wav'))
        if self.phase==0:
            self.remaining_time=self.breaktime
            self.phase=1
        else:
            self.remaining_time=self.worktime
            self.phase=0
    '''
    This function resets the timer to the specified worktime
    '''
    def reset_timer(self):
        self.label.config(text="KEEP WORKING!!!",fg='black')
        self.remaining_time = self.worktime
    def open_menu(self):
        menu_window = tk.Tk()
        menu = CopeTimerMenu(menu_window,self)
        menu.run()
    def close_window(self):
        # Function to close the window
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    window = tk.Tk()
    app = CopeTimer(window)
    app.run()
