import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_entry.delete(0, tk.END)
        csv_entry.insert(0, file_path)
        global df
        df = pd.read_csv(file_path)

def start():
    last_city = last_city_entry.get()
    # Add your logic to process the data
    pass

def stop():
    # Add your logic to stop the data processing
    pass

def reset():
    csv_entry.delete(0, tk.END)
    last_city_entry.delete(0, tk.END)

app = tk.Tk()
app.title("CSV Loader")

csv_label = tk.Label(app, text="CSV File:")
csv_entry = tk.Entry(app)
csv_button = ctk.CTkButton(app, text="Load CSV", command=load_csv)


last_city_label = tk.Label(app, text="Last City Scraped:")
last_city_entry = tk.Entry(app)

start_button = ctk.CTkButton(app, text="Start", command=start)
stop_button = ctk.CTkButton(app, text="Stop", command=stop)
reset_button = ctk.CTkButton(app, text="Reset", command=reset)

csv_label.grid(row=0, column=0, sticky=tk.W)
csv_entry.grid(row=0, column=1)
csv_button.grid(row=0, column=2, padx=5,pady=5)

last_city_label.grid(row=1, column=0, sticky=tk.W)
last_city_entry.grid(row=1, column=1, padx=5,pady=5)

start_button.grid(row=2, column=0, padx=5, pady=10)
stop_button.grid(row=2, column=1, padx=5, pady=10)
reset_button.grid(row=2, column=2, padx=5, pady=10)

app.mainloop()