import customtkinter as ctk
from tkinter import simpledialog

class App:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.master.minsize(200,0)
        self.master.geometry('300x100')
        self.master.resizable(True,True)
        self.master.wm_title('Pomodoro Counter')

        # Create widgets
        #self.title_label = ctk.CTkLabel(self.master, text="Pomodoro Timer", font=("Helvetica", 20))
        #self.title_label.pack(pady=10)
        
        self.timer_label = ctk.CTkLabel(self.master, text="25:00", font=("Helvetica", 24))
        self.timer_label.pack(pady=5)
        
        button_frame = ctk.CTkFrame(self.master)
        button_frame.pack(pady=5)
        button_frame.pack_propagate(0)
        
        button_frame.configure(width=300,height=50)

        #Create grid layout with 3 columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        #Create grid with one row
        button_frame.rowconfigure(0, weight=1)

        self.start_button = ctk.CTkButton(button_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0,column=0, padx=5,pady=5)

        self.stop_button = ctk.CTkButton(button_frame, text="Stop", state=ctk.DISABLED, command=self.stop_timer)
        self.stop_button.grid(row=0,column=1, padx=5,pady=5)
        
        self.reset_button = ctk.CTkButton(button_frame, text="Reset", state=ctk.DISABLED, command=self.reset_timer)
        self.reset_button.grid(row=0,column=2, padx=5,pady=5)

        # Initialize variables
        self.focus_time = 25 * 60  # 25 minutes in seconds
        self.break_time = 5 * 60   # 5 minutes in seconds
        self.focus_count = 0
        self.timer_running = False
        self.timer_paused = False

        # Tagging
        self.tag = None
        self.tag_counter = {}

        self.tag_frame = ctk.CTkFrame(self.master)
        self.tag_frame.pack(pady=5)
        self.tag_frame.pack_propagate(0)
        self.tag_frame.configure(width=300)

        self.tag_label = ctk.CTkLabel(self.tag_frame, text="", font=("Helvetica", 12), justify='left')
        self.tag_label.pack()

    def do_countdown(self, remaining_time):
        if self.timer_running == True:
            self.remaining_time = remaining_time
            mins, secs = divmod(remaining_time, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
            if remaining_time <= 0:
                self.timer_running = False
                self.timer_paused = False  # Added this line to ensure the timer is not in a paused state
                self.stop_button.configure(state=ctk.DISABLED)  # Disable the Stop button
                self.reset_button.configure(state=ctk.NORMAL)  # Enable the Reset button
                self.focus_count += 1
                self.master.bell()  # Sound alarm
                if self.focus_count % 2 == 0:
                    remaining_time = self.break_time
                else:
                    remaining_time = self.focus_time
                self.do_countdown(remaining_time)
                self.update_tag_counter(completed=True)  # Moved this line after resetting the remaining_time
            elif not self.timer_paused:
                self.after_event_id = self.master.after(1000, self.do_countdown, remaining_time - 1)  # Store the event ID 

    
    def start_timer(self):
        if not self.timer_running:
            self.tag = simpledialog.askstring("Task", "What are you working on?")
            if self.tag is not None:
                self.timer_running = True
                self.start_button.configure(state=ctk.DISABLED)
                self.stop_button.configure(state=ctk.NORMAL)
                self.reset_button.configure(state=ctk.NORMAL)
                self.do_countdown(self.focus_time) 
                self.update_tag_counter(init=True)   
        if not self.timer_paused:
                self.after_event_id = self.master.after(1000, self.do_countdown, remaining_time - 1)  # Store the event ID
        elif self.timer_paused:
            self.timer_paused = False
            self.timer_running = True
            self.start_button.configure(state=ctk.DISABLED)            
            self.stop_button.configure(state=ctk.NORMAL)
            self.reset_button.configure(state=ctk.NORMAL)            
            self.do_countdown(self.remaining_time)


    def stop_timer(self):
        if not self.timer_paused:
            self.timer_paused = True 
            self.master.after_cancel(self.after_event_id)  # Cancel the scheduled event                       
            self.start_button.configure(state=ctk.NORMAL)
            self.stop_button.configure(state=ctk.DISABLED)
            self.reset_button.configure(state=ctk.NORMAL)
        elif self.timer_running:
            self.timer_running = False
    
    def reset_timer(self):
        if self.timer_running and not self.timer_paused:
            self.update_tag_counter()        
        self.timer_running = False
        self.timer_paused = False
        self.start_button.configure(state=ctk.NORMAL)
        self.stop_button.configure(state=ctk.DISABLED)
        self.reset_button.configure(state=ctk.DISABLED) 
        self.remaining_time = (25 * 60)
        self.timer_label.configure(text="25:00") 
        self.update_tag_counter(completed=False)             
            
    def update_tag_counter(self, init=False, completed=False):
        if self.tag not in self.tag_counter:
            self.tag_counter[self.tag] = {"complete": 0, "attempts": 1}
        else:
            if init:
                self.tag_counter[self.tag]["attempts"] += 1
            if completed:
                self.tag_counter[self.tag]["complete"] += 1

        tag_text = "Tag\tComplete\tAttempts\n"
        for tag, stats in self.tag_counter.items():
            tag_text += f"{tag}\t{stats['complete']}\t{stats['attempts']}\n"
        self.tag_label.configure(text=tag_text.strip())           

if __name__ == '__main__':
    app = ctk.CTk()
    gui = App(master=app)
    app.mainloop()