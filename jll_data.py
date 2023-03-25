import os
import csv
import random
import time
import pyautogui
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Reads the last processed city
def read_last_processed_city(file_path):
    try:
        with open(file_path, "r") as file:
            last_city = file.read().strip()
    except FileNotFoundError:
        last_city = None
    print(f"Last processed city: {last_city}")
    return last_city

# Updates the last processed city
def update_last_processed_city(file_path, city):
    with open(file_path, "w") as file:
        file.write(city)

# Downloads the report for the specified city
def download_city_report(city):
    sleep_time = random.randint(1, 5)
    url = "https://www.us.jll.com/en/trends-and-insights/research/industrial-market-statistics-trends/{}".format(city)
    print(url)
    # Webdriver path
    webdriver_path = "C:\\Users\\clays\\Documents\\GitHub\\Data_Collection\\chromedriver.exe"
    download_folder = "C:\\Users\\clays\\Downloads"

    # Create ChromeOptions instance
    options = webdriver.ChromeOptions()

    # Add preferences to the ChromeOptions instance
    options.add_experimental_option('prefs', {
        "download.default_directory": "C:\\Users\\clays\\Downloads\\Cameron_RE_Docs\\jll_report.pdf",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    # Create a webdriver instance with the specified options
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    driver.get(url)

    time.sleep(3)

    # Accept cookies using 'tab' twice and then 'enter'
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    time.sleep(sleep_time)

    # Fill out the fields
    first_name_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "firstName"))
    )
    first_name_field.send_keys("Carl")

    time.sleep(sleep_time)

    last_name_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "lastName"))
    )
    last_name_field.send_keys("Richardson")

    time.sleep(sleep_time)

    email_address_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "emailAddress"))
    )
    email_address_field.send_keys("Carl.Richardson@mail.com")

    time.sleep(sleep_time)

    company_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "companyName1"))
    )
    company_field.send_keys("RE Developers")

    time.sleep(sleep_time)

    country_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "country")))
    country_field.send_keys("United States")

    # Get the current window handle
    main_window = driver.current_window_handle

    time.sleep(sleep_time)

    # Click the download button
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Download")]'))
    )
    download_button.click()

    time.sleep(5)

# Function to start the script
def start_script():
    if not script_thread.is_alive():
        script_thread.start()
    else:
        messagebox.showerror("Error", "The script is already running.")

# Function to reset the script
def reset_script():
    if script_thread.is_alive():
        messagebox.showerror("Error", "Terminating the script is not supported. Please close the application.")
    else:
        #update_last_processed_city(last_processed_city_file, '')
        messagebox.showinfo("Success", "The script has been reset.")

def main_function():
    # Read the CSV file containing the city names and store them in a list
    # ... (rest of the code)
    city_file = "jll_cities.csv"

    # Read the list of cities from the csv file
    with open(city_file, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        cities = [row[0] for row in csv_reader]

    # Read the last processed city and find the index of that city in the cities list
    last_processed_city_file = "path_to_last_processed_city_file.txt"
    last_processed_city = read_last_processed_city(last_processed_city_file)

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

# Create the main application window
root = tk.Tk()
root.title("Data Retriever for [insert URL]")
root.geometry("400x200")

# Create and pack the widgets (buttons)
start_button = tk.Button(root, text="Script Start", command=start_script)
reset_button = tk.Button(root, text="Reset", command=reset_script)
start_button.pack(pady=20)
reset_button.pack(pady=20)

# Create a separate thread for running the script
script_thread = Thread(target=main_function)

# Start the main event loop
root.mainloop()


        



