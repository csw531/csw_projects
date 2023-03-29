import os
import csv
import random
import time
import pyautogui
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Reads the last processed city
def read_last_processed_city(text_file):
    try:
        with open(text_file, "r") as file:
            last_city = file.read().strip()
    except FileNotFoundError:
        last_city = None
    print(f"Last processed city: {last_city}")
    return last_city

# Updates the last processed city
def update_last_processed_city(text_file, city):
    with open(text_file, "w") as file:
        file.write(city)
        print("City updated",city)

def main_function(csv_file, text_file):
    # Read the CSV file containing the city names and store them in a list
    # ... (rest of the code)
    city_file = csv_file

    # Read the list of cities from the csv file
    with open(city_file, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        cities = [row[0] for row in csv_reader]

    # Read the last processed city and find the index of that city in the cities list
    #last_processed_city_file = last_city
    last_processed_city = read_last_processed_city(text_file)

    if last_processed_city and last_processed_city in cities:
        start_index = cities.index(last_processed_city) + 1
    else:
        start_index = 0
    print(f"Starting index: {start_index}")


    for city in cities[start_index:]:
        try:
            print(f"Downloading report for {city}")
            download_city_report(city)
            update_last_processed_city(last_processed_city_file, city)
        except Exception as e:
            print(f"Error downloading report for {city}: {e}")
            continue

# Function to open a file dialog and return the selected file path
def choose_file(file_type):
    file_path = filedialog.askopenfilename(filetypes=[(file_type, f'*.{file_type.lower()}')])
    return file_path

# Function to process the CSV and text files
#def process_files(csv_file_path, text_file_path):
    # Your existing code that processes the CSV and text files

def main():
    # Create the main window
    root = tk.Tk()
    root.title("CSV and Text File Processor")

    # Function to handle button click
    def on_process_button_click():
        csv_file = choose_file("CSV")
        text_file = choose_file("TXT")
        if csv_file and text_file:
            read_last_processed_city(text_file)
            main_function(csv_file)
            print(text_file)

    # Create and pack widgets
    instructions_label = tk.Label(root, text="Click the button below to select the proper CSV file and Text file.")
    instructions_label.pack(pady=10)

    process_button = tk.Button(root, text="Select Files and Process", command=on_process_button_click)
    process_button.pack(pady=10)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
