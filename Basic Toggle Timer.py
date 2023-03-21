import tkinter as tk

class FocusWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="green")
        self.label = tk.Label(self, text="Focus", font=("Arial", 24), bg="green")
        self.label.pack()

class RelaxWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="blue")
        self.label = tk.Label(self, text="Relax", font=("Arial", 24), bg="blue")
        self.label.pack()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")

        # create two frames for each window
        self.focus_window = FocusWindow(self)
        self.relax_window = RelaxWindow(self)

        # add buttons to switch between windows
        self.focus_button = tk.Button(self, text="Focus", command=self.show_focus_window)
        self.relax_button = tk.Button(self, text="Relax", command=self.show_relax_window)

        # pack the buttons
        self.focus_button.pack(side=tk.LEFT)
        self.relax_button.pack(side=tk.RIGHT)

        # show the focus window by default
        self.show_focus_window()

    def show_focus_window(self):
        self.relax_window.pack_forget()
        self.focus_window.pack(fill=tk.BOTH, expand=1)
        self.configure(bg="green")

    def show_relax_window(self):
        self.focus_window.pack_forget()
        self.relax_window.pack(fill=tk.BOTH, expand=1)
        self.configure(bg="blue")

if __name__ == '__main__':
    app = Application()
    app.mainloop()
