import customtkinter as ctk

class App:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.master.minsize(200,0)
        self.master.geometry('400x200')
        self.master.resizable(True,True)
        self.master.wm_title('Pomodoro Counter')

        # Create widgets
        self.title_label = ctk.CTkLabel(self.master, text="Pomodoro Timer", font=("Helvetica", 20))
        self.title_label.pack(pady=10)
        
        self.timer_label = ctk.CTkLabel(self.master, text="25:00", font=("Helvetica", 24))
        self.timer_label.pack(pady=10)
        
        button_frame = ctk.CTkFrame(self.master)
        button_frame.pack(pady=10)
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
        self.tags = []
        self.timer_running = False
        self.timer_paused = False


    def do_countdown(self, remaining_time):
            if self.timer_running == True:
                self.remaining_time = remaining_time
                mins, secs = divmod(remaining_time, 60)
                self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
                if remaining_time <= 0:
                    self.timer_running = False
                    self.focus_count += 1
                    self.tags.append(self.get_tag())
                    self.master.bell()  # Sound alarm
                    if self.focus_count % 2 == 0:
                        remaining_time = self.break_time
                    else:
                        remaining_time = self.focus_time
                    self.do_countdown(remaining_time)
                elif not self.timer_paused:
                    self.master.after(1000, self.do_countdown, remaining_time - 1)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_button.configure(state=ctk.DISABLED)
            self.stop_button.configure(state=ctk.NORMAL)
            self.reset_button.configure(state=ctk.NORMAL)
            self.do_countdown(self.focus_time)          
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
            self.start_button.configure(state=ctk.NORMAL)
            self.stop_button.configure(state=ctk.DISABLED)
            self.reset_button.configure(state=ctk.NORMAL)
        elif self.timer_running:
            self.timer_running = False
    
    def reset_timer(self):
        self.timer_running = False
        self.timer_paused = False
        self.start_button.configure(state=ctk.NORMAL)
        self.stop_button.configure(state=ctk.DISABLED)
        self.reset_button.configure(state=ctk.DISABLED) 
        self.remaining_time = (25 * 60)
        self.timer_label.configure(text="25:00")      
            
    def get_tag(self):
        tag = ctk.simpledialog.askstring("Tag", "Enter a tag for this focus cycle:")
        return tag if tag is not None else ""            

if __name__ == '__main__':
    app = ctk.CTk()
    gui = App(master=app)
    app.mainloop()