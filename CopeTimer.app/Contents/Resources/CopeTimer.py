import tkinter as tk
from tkinter import ttk
from AppKit import NSWorkspace
from playsound import playsound
import os
import json

global_ringtone = "ring1.wav"

class MainMenu:
    def __init__(self, window):
        self.window = window
        self.time1=0
        self.time2=0
        window.title("CopeTimer")
        #This sets the position to the top left
        window.geometry(f"+0+0")
        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)
        # Elements:
        
        self.label = tk.Label(window, text="SELECT A MODE",font=("Georgia",20))
        button = tk.Button(window, text="Time Loop Mode", command=self.open_loop,width = 10, height = 1,font='Georgia',relief='ridge')
        button2 = tk.Button(window, text="Full Focus Mode", command=self.open_focus,width = 10, height = 1,font='Georgia',relief='ridge')
        button3 = tk.Button(window, text="Tracking Mode", command=self.open_tracking,width = 10, height = 1,font='Georgia',relief='ridge')
        self.img = tk.PhotoImage(file = (os.path.join(os.path.dirname(__file__), 'images', "icon.png"))).subsample(2,2)
        label2 = tk.Label(window, image = self.img)


        # grid elements:
        self.label.grid(row = 0, column = 0,columnspan=2, padx = 30)
        button.grid(row = 1, column = 0, pady = 2)
        button2.grid(row = 2, column = 0, pady = 2)
        button3.grid(row = 3, column = 0, pady = 2)
        label2.grid(row = 1, column = 1, rowspan = 3)

    def open_loop(self):
        window = tk.Tk()
        self.close_window()
        app = CopeLoop(window)
        app.run
    def open_focus(self):
        window = tk.Tk()
        self.close_window()
        app = CopeFocus(window)
        app.run
    def open_tracking(self):
        window = tk.Tk()
        self.close_window()
        app = CopeTrack(window)
        app.run
    def close_window(self):
        # Function to close the window
        self.window.destroy()
        del self
    def run(self):
        self.window.mainloop()

class CopeLoop:
    def __init__(self, window):
        self.window = window
        window.title("CopeTimer")
        self.phase = 0
        self.button_loaded = 0
        self.ringtone = "ring1.wav"
        #This sets the position to the top left
        window.geometry(f"+0+0")
        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)
        self.worktime = 3600 # 1 hour time fixed
        self.breaktime = 300 # 5 minute break
        # Elements:
        
        self.label = tk.Label(window, text="KEEP WORKING!!!",font=("Georgia",20))
        self.timer_label = tk.Label(window, text="",font=("Georgia",40))


        # Pack elements:

        self.label.pack(padx=5, pady=5)
        self.timer_label.pack(pady=5)
        #self.remaining_time = 3600  # 1 hour
        self.remaining_time = self.worktime

        # call update timer
        window.after(100, self.update_timer)

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

        if self.button_loaded == 0:
            # pack buttons after timer has started    
                
            button1 = tk.Button(self.window, text="RESET", command=self.reset_timer,width = 5, height = 1,font='Georgia',relief='ridge')
            button2 = tk.Button(self.window, text="MENU", command=self.open_menu,width = 5, height = 1,font='Georgia',relief='ridge')
            button3 = tk.Button(self.window, text="SETTINGS", command=self.open_settings,width = 5, height = 1,font='Georgia',relief='ridge')

            button1.pack(side="left")
            button2.pack(side="right")
            button3.pack(side="right")
            self.button_loaded = 1;

        #self call update
        self.window.after(1000, self.update_timer)

    def set_worktime(self,time):
        self.worktime = time
    def get_worktime(self):
        return self.worktime
    def set_breaktime(self,time):
        self.breaktime = time
    def get_breaktime(self):
        return self.breaktime
    def play_ringtone(self):
        playsound(os.path.join(os.path.dirname(__file__), 'sounds', global_ringtone))
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
    def open_settings(self):
        menu_window = tk.Tk()
        menu = CopeLoopSettings(menu_window,self)
        menu.run()
    def open_menu(self):
        menu_window = tk.Tk()
        self.close_window()
        menu = MainMenu(menu_window)
        menu.run()
    def close_window(self):
        # Function to close the window
        self.window.destroy()
        del self
    def run(self):
        self.window.mainloop()
class CopeLoopSettings:
    def __init__(self, window,copetimer):
        self.window = window
        self.time1=0
        self.time2=0
        self.copetimer = copetimer
        self.ringtone = "ring1.wav"
        window.title("Settings")

        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)

        # Elements:
        
        label = tk.Label(window, text="SETTINGS",font=("Georgia",20))
        label2 = tk.Label(window, text="Work duration (seconds):",font=("Georgia",15))
        label3 = tk.Label(window, text="Break duration (seconds):",font=("Georgia",15))
        label4 = tk.Label(window, text="Select a ringtone:",font=("Georgia",15))
        button = tk.Button(window, text="DONE", command=self.set_values,width = 5, height = 1,font='Georgia',relief='ridge')
        # Ringtone selection
        ringtones = ["Cellphone", "Old Telephone", "Notification Sound"]
        selected_ringtone = tk.StringVar(window)
        self.dropdown = ttk.Combobox(window, textvariable=selected_ringtone, values=ringtones, state="readonly")

        self.entry1= tk.Entry(window, width= 10)
        self.entry1.insert(0,copetimer.get_worktime())
        self.entry2= tk.Entry(window, width= 10)
        self.entry2.insert(0, copetimer.get_breaktime())
        self.entry1.focus_set()
        self.entry1.focus_set()
        

        # grid elements:

        label.grid(row = 0, column = 0, pady = 2)
        label2.grid(row = 1, column = 0, pady = 2)
        label3.grid(row = 2, column = 0, pady = 2)
        label4.grid(row = 3, column = 0, pady = 2)
        self.entry1.grid(row = 1, column = 1, pady = 2)
        self.entry2.grid(row = 2, column = 1, pady = 2)
        self.dropdown.grid(row = 3, column = 1, pady=2)
        button.grid(row = 3, column = 2, pady = 2)

    def set_values(self):
        time1 = self.entry1.get()
        time2 = self.entry2.get()
        selected_ringtone = self.dropdown.get()
        #print(self.time1)
        #print(self.time2)
        if time1.isnumeric() and time2.isnumeric():
            self.copetimer.set_worktime(int(time1))  
            self.copetimer.set_breaktime(int(time2))  
            self.set_ringtone(selected_ringtone)   
            self.close_window()
    def set_ringtone(self,selected_ringtone):
        global global_ringtone
        if selected_ringtone == "Cellphone":
            global_ringtone = "ring1.wav"
        if selected_ringtone == "Old Telephone":
            global_ringtone = "ring2.wav"
        if selected_ringtone == "Notification Sound":
            global_ringtone = "ring3.wav"
    def close_window(self):
        # Function to close the window
        self.window.destroy()
        del self
    def run(self):
        self.window.mainloop()

class CopeFocus:
    def __init__(self, window):
        self.window = window
        window.title("CopeTimer")
        #This sets the position to the top left
        window.geometry(f"+0+0")
        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)
        self.worktime = 0 
        self.alerttime = 0
        self.button_loaded = 0
        # Elements:


        self.current_app = "None Selected"
        
        self.label = tk.Label(window, text="KEEP WORKING!!!",font=("Georgia",20))
        self.label2 = tk.Label(window, text="Now tracking: "+self.current_app,font=("Georgia",15))
        self.timer_label = tk.Label(window, text="",font=("Georgia",40))


        # Pack elements:
        self.label.pack(padx=10, pady=10)
        self.timer_label.pack(pady=10)
        self.label2.pack()

        # call update timer
        window.after(100, self.update_timer)

    def update_timer(self):
        # Update the timer label
        hours, remainder = divmod(self.worktime, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=f"{time_str}")

        app2 = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
        if app2 != self.current_app:
            self.label.config(text = "GET BACK TO WORK!!!",fg='red4')
            self.alerttime +=1
            if self.alerttime == 7:
                self.alerttime=0
                self.play_ringtone()
        else:
            self.label.config(text = "KEEP WORKING!!!",fg='black')
            self.worktime += 1

        if self.button_loaded == 0:
            # pack buttons after timer has started    
                
            button1 = tk.Button(self.window, text="RESET", command=self.reset_timer,width = 5, height = 1,font='Georgia',relief='ridge')
            button2 = tk.Button(self.window, text="MENU", command=self.open_menu,width = 5, height = 1,font='Georgia',relief='ridge')
            button3 = tk.Button(self.window, text="SETTINGS", command=self.open_settings,width = 5, height = 1,font='Georgia',relief='ridge')
            
            button1.pack(side="left")
            button2.pack(side="right")
            button3.pack(side="right")
            self.button_loaded = 1;

        #self call update
        self.window.after(1000, self.update_timer)

    def set_worktime(self,time):
        self.worktime = time
    def play_ringtone(self):
        playsound(os.path.join(os.path.dirname(__file__), 'sounds', global_ringtone))

    '''
    This function resets the timer to the specified worktime
    '''
    def set_app(self,app):
        self.current_app = app 
        self.label2.config(text = "Now tracking: "+self.current_app)  
        self.worktime = 0
    def reset_timer(self):
        self.worktime = 0
    def open_settings(self):
        menu_window = tk.Tk()
        menu = CopeFocusSettings(menu_window,self)
        menu.run()
    def open_menu(self):
        menu_window = tk.Tk()
        self.close_window()
        menu = MainMenu(menu_window)
        menu.run()
    def close_window(self):
        # Function to close the window
        self.window.destroy()
        del self
    def run(self):
        self.window.mainloop()
class CopeFocusSettings:
    def __init__(self, window,copetimer):
        self.window = window
        self.time1=0
        self.time2=0
        self.copetimer = copetimer
        self.ringtone = "ring1.wav"
        window.title("Settings")

        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)

        # Elements:
        
        label = tk.Label(window, text="SETTINGS",font=("Georgia",20))
        label1 = tk.Label(window, text="Click on an app to detect it:",font=("Georgia",15))
        label2 = tk.Label(window, text="Select a ringtone:",font=("Georgia",15))
        button = tk.Button(window, text="DONE", command=self.set_values,width = 5, height = 1,font='Georgia',relief='ridge')
        # App selection
        self.apps = []
        selected_app = tk.StringVar(window)
        self.dropdown = ttk.Combobox(window, textvariable=selected_app, values=self.apps, state="readonly")
        # Ringtone selection
        ringtones = ["Cellphone", "Old Telephone", "Notification Sound"]
        selected_ringtone = tk.StringVar(window)
        self.dropdown2 = ttk.Combobox(window, textvariable=selected_ringtone, values=ringtones, state="readonly")


        # grid elements:

        label.grid(row = 0, column = 0, pady = 2)
        label1.grid(row = 1, column = 0, pady = 2)
        label2.grid(row = 2, column = 0, pady = 2)
        self.dropdown.grid(row = 1, column = 1, pady=2)
        self.dropdown2.grid(row = 2, column = 1, pady=2)
        button.grid(row = 2, column = 2, pady = 2)

        window.after(100, self.update_detector)
    def update_detector(self):
        
        app = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
        if app not in self.apps:
            self.apps.append(app)
        self.dropdown['values'] = self.apps

        window.after(100, self.update_detector)
    def set_values(self):
        selected_app = self.dropdown.get()
        self.copetimer.set_app(selected_app)
        selected_ringtone = self.dropdown2.get()
        self.set_ringtone(selected_ringtone)   
        self.close_window()
    def set_ringtone(self,selected_ringtone):
        global global_ringtone
        if selected_ringtone == "Cellphone":
            global_ringtone = "ring1.wav"
        if selected_ringtone == "Old Telephone":
            global_ringtone = "ring2.wav"
        if selected_ringtone == "Notification Sound":
            global_ringtone = "ring3.wav"
    def close_window(self):
        # Function to close the window
        self.window.destroy()
        del self
    def run(self):
        self.window.mainloop()

class CopeTrack:
    def __init__(self, window):
        self.window = window
        window.title("CopeTimer")
        self.phase = 0
        # Loading json save file
        try:
            with open('app_tracking.json', 'r') as file:
                file_content = file.read()
                if file_content:
                    self.apps = json.loads(file_content)
                else:
                    self.apps = {}
        except (FileNotFoundError, json.JSONDecodeError):
            self.apps = {}

        self.current_app = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
        #This sets the position to the top left
        window.geometry(f"+0+0")
        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)
        #Get self.worktime from json
        self.worktime = self.apps.get(self.current_app, 0)


        # Elements:
        self.label = tk.Label(window, text="Current App:",font=("Georgia",15))
        self.label2 = tk.Label(window, text="       ",font=("Georgia",20))
        button1 = tk.Button(window, text="SAVE AND EXIT", command=self.save_times,width = 10, height = 1,font='Georgia',relief='ridge')
        button2 = tk.Button(window, text="STATS", command=self.open_stats,width = 5, height = 1,font='Georgia',relief='ridge')
        button3 = tk.Button(window, text="MENU", command=self.open_menu,width = 5, height = 1,font='Georgia',relief='ridge')
        self.timer_label = tk.Label(window, text="",font=("Georgia",40))


        # Pack elements:
        self.label.grid(row = "0",column = "0", padx=10, pady=4)
        self.label2.grid(row = "0",column = "1", padx=2, pady=4)
        self.timer_label.grid(row = "1",column = "0",columnspan = 4,pady=5)
        button1.grid(row = "2",column = "0",pady=5)
        button2.grid(row = "2",column = "1",pady=5)
        button3.grid(row = "2",column = "2",pady=5)
        #self.remaining_time = 3600  # 1 hour
        self.worktime

        # call update timer
        window.after(100, self.update_timer)

    def update_timer(self):
        # Update the timer label
        hours, remainder = divmod(self.worktime, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=f"{time_str}")
        app_name = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
        #Check if app has changed, if so set worktime to 0
        if app_name != self.current_app:
            if app_name in self.apps:
                self.worktime = self.apps[app_name]
            else:
                self.worktime = 0
            self.current_app = app_name
        self.label2.config(text=app_name,fg='black')
        self.apps[app_name]=self.worktime
        self.worktime += 1
        #self call update
        self.window.after(1000, self.update_timer)
    def set_worktime(self,time):
        self.worktime = time
    def get_apps(self):
        return self.apps
    def set_apps(self,apps):
        self.apps = apps
    def open_menu(self):
        menu_window = tk.Tk()
        self.close_window()
        menu = MainMenu(menu_window)
        menu.run()
    def open_stats(self):
        menu_window = tk.Tk()
        menu = CopeTrackStats(menu_window,self)
        menu.run()
    def save_times(self):
        #Saving times to json
        with open('app_tracking.json', 'w') as file:
            json.dump(self.apps, file)
        self.open_menu()

    def close_window(self):
        # Function to close the window
        self.window.destroy()
        del self
    def run(self):
        self.window.mainloop()
class CopeTrackStats:
    def __init__(self, window,copetrack):
        self.window = window
        self.copetrack = copetrack
        window.title("Statistics")
        #This sets the timer window to be always on top
        window.wm_attributes('-topmost', 1)

        # Elements:
        
        label = tk.Label(window, text="STATISTICS",font=("Georgia",20))
        label.pack(pady = 2)

        for key,value in copetrack.get_apps().items():
            hours, remainder = divmod(value, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            label2 = tk.Label(window, text=key+"   "+time_str,font=("Georgia",15))
            label2.pack(pady = 2)

        button = tk.Button(window, text="CLEAR TIMES", command=self.clear_values,width = 9, height = 1,font='Georgia',relief='ridge')
        button.pack(pady = 2)

    def clear_values(self):
        with open('app_tracking.json', 'w') as filename:
            json.dump({}, filename)
        self.copetrack.set_apps({})
        self.copetrack.set_worktime(0)
        self.close_window()
    def close_window(self):
        # Function to close the window
        self.window.destroy()
        del self
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    #test print of all running apps
    #print(NSWorkspace.sharedWorkspace().runningApplications())
    window = tk.Tk()
    app = MainMenu(window)
    app.run()
