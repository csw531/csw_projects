import customtkinter as ctk

class FocusWindow(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, bg_color="#2E8B57")
        self.label = ctk.CTkLabel(self, text="Focus", font=("Arial", 24), bg_color="#2E8B57")
        self.label.pack()
        

class RelaxWindow(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, bg_color="#3076F0")
        self.label = ctk.CTkLabel(self, text="Relax", font=("Arial", 24), bg_color="#3076F0")
        self.label.pack()

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")

        # create two CTkFrames for each window
        self.focus_window = FocusWindow(self)
        self.relax_window = RelaxWindow(self)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=0)
        self.button_frame.pack_propagate(0)
        self.button_frame.configure(width=300,height=50)
        #Create grid layout with 2 columns
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        #Create grid with one row
        self.button_frame.rowconfigure(0, weight=1)

        # add buttons to switch between windows
        self.focus_button = ctk.CTkButton(self.button_frame, text="Focus", command=self.show_focus_window)
        self.relax_button = ctk.CTkButton(self.button_frame, text="Relax", command=self.show_relax_window)

        # pack the buttons
        self.focus_button.grid(row=0,column=0,padx=5,pady=5)
        self.relax_button.grid(row=0,column=1,padx=5,pady=5)

        # show the focus window by default
        self.show_focus_window()

    def show_focus_window(self):
        self.relax_window.pack_forget()
        self.focus_window.pack(fill=ctk.BOTH, expand=1)
        self.configure(bg_color="#2E8B57")

    def show_relax_window(self):
        self.focus_window.pack_forget()
        self.relax_window.pack(fill=ctk.BOTH, expand=1)
        self.configure(bg_color="#3076F0")

if __name__ == '__main__':
    app = Application()
    app.mainloop()
