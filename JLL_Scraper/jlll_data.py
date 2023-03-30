import os
import csv
import sys
import random
import time
import pyautogui
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from functools import partial
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# (rest of your functions here, unchanged)

# Create the main application window
root = tk.Tk()
root.title("JLL Data Retriever")
root.geometry("225x275")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create and configure the main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add title label
title_label = ttk.Label(main_frame, text="JLL Data Retriever", font=("Arial", 16))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Inputs
first_name_label = ttk.Label(main_frame, text="First Name:")
first_name_label.grid(row=1, column=0, pady=5)
first_name_var = tk.StringVar()
first_name_entry = tk.Entry(main_frame, width=100, textvariable=first_name_var)
first_name_entry.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))

last_name_label = ttk.Label(main_frame, text="Last Name:")
last_name_label.grid(row=2, column=0, pady=5)
last_name_var = tk.StringVar()
last_name_entry = tk.Entry(main_frame, width=100, textvariable=last_name_var)
last_name_entry.grid(row=2, column=1, padx=(5, 5), pady=(5, 5))

email_address_label = ttk.Label(main_frame, text="Email Address:")
email_address_label.grid(row=4, column=0, pady=5)
email_address_var = tk.StringVar()
email_address_entry = tk.Entry(main_frame, width=100, textvariable=email_address_var)
email_address_entry.grid(row=4, column=1, padx=(5, 5), pady=(5, 5))

company_entry_label = ttk.Label(main_frame, text="Company Name:")
company_entry_label.grid(row=5, column=0, pady=5)
company_var = tk.StringVar()
company_entry = tk.Entry(main_frame, width=100, textvariable=company_var)
company_entry.grid(row=5, column=1, padx=(5, 5), pady=(5, 5))

# Add trace on entry field variables
first_name_var.trace("w", check_entries)
last_name_var.trace("w", check_entries)
email_address_var.trace("w", check_entries)
company_var.trace("w", check_entries)

# Create and pack the widgets (buttons)
start_button = ttk.Button(root, text="Start Script", command=start_script, state=tk.DISABLED)
start_button.grid(row=6, column=0, padx=(5, 5), pady=(5, 5))

# Create a separate thread for running the script
script_thread = Thread(target=main_function)

# Start the main event loop
root.mainloop()
